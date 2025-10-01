from contextlib import contextmanager
from datetime import timedelta
from typing import Any, Dict

import pytest

from src import mcp_client


class FakeProcess:
    def __init__(self, returncode: int = 0):
        self.returncode = returncode
        self.stdin = None
        self.stdout = None
        self._terminated = False

    def poll(self) -> int:
        return self.returncode if self._terminated else None

    def terminate(self) -> None:
        self._terminated = True

    def wait(self, timeout: float) -> int:
        return self.returncode


def fake_subprocess_factory(expected_args: Dict[str, Any]):
    def factory(executable: str, args: list[str]):
        assert executable == expected_args["executable"]
        assert args == expected_args["args"]
        process = FakeProcess()
        process.stdin = expected_args.get("stdin")
        process.stdout = expected_args.get("stdout")
        return process

    return factory


def test_client_initialization_loads_config(tmp_path):
    config = {
        "path": "../dist/server.js",
        "node_path": "node",
        "timeout_seconds": 2,
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(mcp_client.dumps_json(config))
    client = mcp_client.create_client_from_file(str(config_path))
    assert client["server_path"] == "../dist/server.js"
    assert client["node_path"] == "node"
    assert client["timeout"] == 2.0
    assert client["process"] is None


def test_start_launches_subprocess(monkeypatch, tmp_path):
    expected = {
        "executable": "node",
        "args": ["../dist/server.js"],
        "stdin": "in",
        "stdout": "out",
    }
    config = {
        "path": expected["args"][0],
        "node_path": expected["executable"],
    }
    client = mcp_client.create_client(config)
    monkeypatch.setattr(mcp_client, "popen_launch", fake_subprocess_factory(expected))
    status = mcp_client.start_client(client)
    assert status
    assert client["process"].stdin == "in"
    assert client["process"].stdout == "out"


def test_start_raises_when_already_running(tmp_path):
    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})
    client["process"] = FakeProcess()
    with pytest.raises(RuntimeError):
        mcp_client.start_client(client)


def test_stop_terminates_process(monkeypatch):
    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})
    process = FakeProcess()
    client["process"] = process
    stopped = mcp_client.stop_client(client)
    assert stopped
    assert client["process"] is None
    assert process._terminated


def test_stop_handles_no_process():
    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})
    stopped = mcp_client.stop_client(client)
    assert not stopped


def test_context_manager_starts_and_stops(monkeypatch):
    expected = {
        "executable": "node",
        "args": ["server.js"],
        "stdin": "in",
        "stdout": "out",
    }
    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})
    monkeypatch.setattr(mcp_client, "popen_launch", fake_subprocess_factory(expected))
    with mcp_client.use_client(client) as running:
        assert running["process"] is not None
    assert client["process"] is None


def test_start_handles_launch_failure(monkeypatch):
    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})

    def failing_launch(executable: str, args: list[str]):
        raise OSError("cannot launch")

    monkeypatch.setattr(mcp_client, "popen_launch", failing_launch)
    with pytest.raises(RuntimeError):
        mcp_client.start_client(client)


def test_stop_wait_timeout(monkeypatch):
    client = mcp_client.create_client({"path": "server.js", "node_path": "node", "timeout_seconds": 0.01})
    process = FakeProcess()
    process.wait = lambda timeout: (_ for _ in ()).throw(TimeoutError())
    client["process"] = process
    stopped = mcp_client.stop_client(client)
    assert stopped


def test_double_context_error(monkeypatch):
    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})
    monkeypatch.setattr(mcp_client, "popen_launch", fake_subprocess_factory({"executable": "node", "args": ["server.js"]}))
    context = mcp_client.use_client(client)
    with context:
        with pytest.raises(RuntimeError):
            with context:
                pass


def test_create_client_validates_config():
    with pytest.raises(ValueError):
        mcp_client.create_client({})

    with pytest.raises(ValueError):
        mcp_client.create_client({"path": "server.js"})

    client = mcp_client.create_client({"path": "server.js", "node_path": "node"})
    assert client["timeout"] == pytest.approx(5.0)
