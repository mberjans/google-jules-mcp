"""Functional helpers for managing the MCP server subprocess."""

from __future__ import annotations

import json
import logging
import select
import subprocess
from typing import Dict, Iterable, Optional

DEFAULT_TIMEOUT_SECONDS = 5.0
LOGGER = logging.getLogger(__name__)


def dumps_json(payload: Dict[str, object]) -> str:
    """Serialize dictionaries to JSON with stable formatting."""
    return json.dumps(payload, indent=2, sort_keys=True)


def loads_json(content: str) -> Dict[str, object]:
    """Parse JSON content into a dictionary."""
    data = json.loads(content)
    if not isinstance(data, dict):
        raise ValueError("Configuration JSON must deserialize into a dictionary")
    return data


def _normalize_timeout(value: Optional[object]) -> float:
    if value is None:
        return DEFAULT_TIMEOUT_SECONDS
    if isinstance(value, (int, float)):
        return float(value)
    message = "Timeout must be numeric"
    raise ValueError(message)


def _validate_config(config: Dict[str, object]) -> Dict[str, object]:
    if not isinstance(config, dict):
        raise ValueError("Configuration must be provided as a dictionary")
    server_path = config.get("path")
    node_path = config.get("node_path")
    if not server_path:
        raise ValueError("Configuration requires 'path'")
    if not node_path:
        raise ValueError("Configuration requires 'node_path'")
    normalized: Dict[str, object] = {}
    normalized["server_path"] = str(server_path)
    normalized["node_path"] = str(node_path)
    normalized["timeout"] = _normalize_timeout(config.get("timeout_seconds"))
    process = config.get("process")
    normalized["process"] = process
    normalized["active_contexts"] = 0
    return normalized


def create_client(config: Dict[str, object]) -> Dict[str, object]:
    """Create a client dictionary from an in-memory configuration."""
    validated = _validate_config(config)
    client: Dict[str, object] = {}
    for key, value in validated.items():
        client[key] = value
    return client


def create_client_from_file(config_path: str) -> Dict[str, object]:
    """Load configuration from a JSON file and create a client."""
    with open(config_path, "r", encoding="utf-8") as handle:
        content = handle.read()
    config = loads_json(content)
    return create_client(config)


def popen_launch(executable: str, args: Iterable[str]) -> subprocess.Popen:
    """Launch the MCP server process using subprocess.Popen."""
    arguments_list = []
    for item in args:
        arguments_list.append(item)
    return subprocess.Popen(  # nosec B603
        [executable] + arguments_list,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _ensure_not_running(client: Dict[str, object]) -> None:
    process = client.get("process")
    if process is not None:
        if process.poll() is None:
            raise RuntimeError("MCP client already running")
    client["process"] = None


def start_client(client: Dict[str, object]) -> bool:
    """Start the MCP server subprocess for the given client."""
    _ensure_not_running(client)
    executable = client["node_path"]
    args = [client["server_path"]]
    LOGGER.info("Starting MCP server", extra={"executable": executable, "args": args})
    try:
        process = popen_launch(executable, args)
    except OSError as error:
        LOGGER.error("Failed to start MCP server", exc_info=True)
        message = f"Failed to start MCP server: {error}"
        raise RuntimeError(message) from error
    client["process"] = process
    return True


def _wait_for_process(process: subprocess.Popen, timeout: float) -> None:
    try:
        process.wait(timeout=timeout)
    except TimeoutError:
        raise
    except subprocess.TimeoutExpired:
        raise TimeoutError()


def stop_client(client: Dict[str, object]) -> bool:
    """Stop the MCP server subprocess if it is running."""
    process = client.get("process")
    if process is None:
        LOGGER.debug("Stop requested but no active process")
        return False
    timeout = float(client.get("timeout", DEFAULT_TIMEOUT_SECONDS))
    try:
        LOGGER.info("Terminating MCP server process")
        process.terminate()
    except Exception:
        LOGGER.warning("Failed to terminate process cleanly", exc_info=True)
        client["process"] = None
        return True
    try:
        _wait_for_process(process, timeout)
    except TimeoutError:
        LOGGER.warning("Process did not exit before timeout", extra={"timeout": timeout})
        client["process"] = None
        return True
    client["process"] = None
    return True


def create_request_id_generator():
    """Return a callable that generates unique JSON-RPC request identifiers."""
    state = {"value": 0}

    def _next_id():
        state["value"] += 1
        return str(state["value"])

    return _next_id


def build_json_rpc_request(method: str, params: Dict[str, object], generator) -> Dict[str, object]:
    """Construct a JSON-RPC 2.0 request dictionary."""
    if generator is None:
        generator = create_request_id_generator()
    request_id = generator()
    request: Dict[str, object] = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params,
    }
    return request


def send_json_rpc_request(client: Dict[str, object], request: Dict[str, object]) -> None:
    """Serialize and send a JSON-RPC request via the client's subprocess stdin."""
    process = client.get("process")
    if process is None or not hasattr(process, "stdin"):
        raise RuntimeError("MCP client process is not running")
    LOGGER.debug(
        "Sending JSON-RPC request",
        extra={"method": request.get("method"), "id": request.get("id")},
    )
    serialized = dumps_json(request) + "\n"
    process.stdin.write(serialized)
    process.stdin.flush()


def read_json_rpc_response(client: Dict[str, object]) -> Dict[str, object]:
    """Read and deserialize a JSON-RPC response from the client's subprocess stdout."""
    process = client.get("process")
    if process is None or not hasattr(process, "stdout"):
        raise RuntimeError("MCP client process is not running")
    timeout = float(client.get("timeout", DEFAULT_TIMEOUT_SECONDS))
    while True:
        line = _readline_with_timeout(process.stdout, timeout)
        if line == "":
            raise RuntimeError("No response received from MCP server")
        stripped = line.strip()
        if stripped:
            try:
                response = json.loads(stripped)
            except json.JSONDecodeError as error:
                LOGGER.error("Failed to decode MCP response", extra={"payload": stripped})
                raise RuntimeError("Invalid JSON-RPC response format") from error
            if not isinstance(response, dict):
                raise RuntimeError("Invalid JSON-RPC response format")
            LOGGER.debug(
                "Received JSON-RPC response",
                extra={"keys": list(response.keys())},
            )
            return response


def _get_or_create_request_id_generator(client: Dict[str, object]):
    generator = client.get("_request_id_generator")
    if generator is None:
        generator = create_request_id_generator()
        client["_request_id_generator"] = generator
    return generator


def invoke_tool(client: Dict[str, object], method: str, params: Dict[str, object]) -> Dict[str, object]:
    """Send a JSON-RPC request and return the result field from the response."""
    generator = _get_or_create_request_id_generator(client)
    request = build_json_rpc_request(method, params, generator)
    send_json_rpc_request(client, request)
    response = read_json_rpc_response(client)
    if "error" in response:
        error = response["error"]
        message = "MCP server returned an error"
        if isinstance(error, dict) and "message" in error:
            message = str(error.get("message"))
        LOGGER.error("MCP server returned error", extra={"message": message})
        raise RuntimeError(message)
    result = response.get("result")
    if result is None:
        raise RuntimeError("MCP server response missing result field")
    if isinstance(result, dict):
        normalized: Dict[str, object] = {}
        for key, value in result.items():
            normalized[key] = value
        LOGGER.debug("Parsed JSON-RPC result dictionary", extra={"keys": list(normalized.keys())})
        return normalized
    LOGGER.debug("Wrapped non-dict JSON-RPC result", extra={"type": type(result).__name__})
    return {"value": result}


def _readline_with_timeout(stream, timeout: float) -> str:
    """Read a line from stream, respecting timeout when possible."""
    if timeout is None:
        return stream.readline()
    if hasattr(stream, "fileno"):
        try:
            fileno_method = stream.fileno
        except AttributeError:
            fileno_method = None
        if fileno_method is not None:
            try:
                _ = fileno_method()
                readable, _, _ = select.select([stream], [], [], timeout)
                if not readable:
                    raise TimeoutError()
            except (OSError, ValueError):
                pass
    return stream.readline()


def use_client(client: Dict[str, object]):
    """Return a context manager that manages MCP client lifecycle."""
    state = {"entered": False, "started": False}

    def __enter__(self):
        if state["entered"]:
            raise RuntimeError("Client context already in use")
        active = int(client.get("active_contexts", 0))
        if active > 0:
            raise RuntimeError("Client context already active")
        state["entered"] = True
        client["active_contexts"] = active + 1
        start_client(client)
        state["started"] = True
        return client

    def __exit__(self, exc_type, exc, exc_tb):
        if state["started"]:
            stop_client(client)
            state["started"] = False
        client["active_contexts"] = 0
        state["entered"] = False
        return False

    context_type = type("_ClientContext", (), {"__enter__": __enter__, "__exit__": __exit__})
    return context_type()
