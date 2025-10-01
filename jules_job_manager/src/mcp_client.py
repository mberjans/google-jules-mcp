"""Functional helpers for managing the MCP server subprocess."""

from __future__ import annotations

import json
import logging
import subprocess
from contextlib import AbstractContextManager
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
    LOGGER.info("MCP server process stopped successfully")
    return True


class _ClientContext(AbstractContextManager):
    """Context manager implementation for MCP client lifecycle."""

    def __init__(self, client: Dict[str, object]):
        self._client = client
        self._entered = False
        self._started = False

    def __enter__(self) -> Dict[str, object]:
        if self._entered:
            raise RuntimeError("Client context already in use")
        self._entered = True
        active = int(self._client.get("active_contexts", 0))
        if active > 0:
            raise RuntimeError("Client context already active")
        self._client["active_contexts"] = active + 1
        start_client(self._client)
        self._started = True
        return self._client

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        self._client["active_contexts"] = 0
        if self._started:
            stop_client(self._client)
        self._started = False


def use_client(client: Dict[str, object]) -> _ClientContext:
    """Return context manager for the MCP client lifecycle."""
    return _ClientContext(client)
