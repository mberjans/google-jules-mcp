"""Tests for Job Manager initialization logic."""

import json
from datetime import datetime
from typing import Dict, List

import pytest

from src import job_manager, models, storage


def create_dummy_mcp_client() -> dict:
    def invoke_tool(*args, **kwargs):  # pragma: no cover - dummy callable
        return None

    client: dict = {"name": "dummy-mcp", "invoke_tool": invoke_tool}
    return client


def create_dummy_storage() -> dict:
    storage: dict = {"name": "dummy-storage"}
    return storage


def test_create_job_manager_with_dependencies() -> None:
    mcp_client = create_dummy_mcp_client()
    storage = create_dummy_storage()
    manager = job_manager.create_job_manager(mcp_client, storage)
    assert manager["mcp_client"] is mcp_client
    assert manager["storage"] is storage


def test_mcp_client_injection_is_validated() -> None:
    storage = create_dummy_storage()
    with pytest.raises(ValueError):
        job_manager.create_job_manager(None, storage)


def test_storage_injection_is_validated() -> None:
    mcp_client = create_dummy_mcp_client()
    with pytest.raises(ValueError):
        job_manager.create_job_manager(mcp_client, None)


def test_dependency_validation_rejects_invalid_inputs() -> None:
    invalid_client = {"name": "dummy", "type": "not-callable"}
    storage = create_dummy_storage()
    with pytest.raises(TypeError):
        job_manager.create_job_manager(invalid_client, storage)


def create_stub_mcp_client(responder):
    calls: List[Dict[str, object]] = []

    def invoke_tool(name: str, arguments: Dict[str, object]):
        calls.append({"name": name, "arguments": arguments})
        return responder(name, arguments)

    client: Dict[str, object] = {"invoke_tool": invoke_tool, "calls": calls}
    return client


def create_serialized_task(task_id: str, status: str) -> Dict[str, object]:
    timestamp = datetime.now().astimezone()
    task = models.create_jules_task(
        task_id,
        "Example Title",
        "Example Description",
        "owner/repo",
        "main",
        status,
        timestamp,
        timestamp,
        "https://example.com/task",
    )
    serialized = models.jules_task_to_dict(task)
    return serialized


def create_storage_manager_with_tasks(tmp_path, tasks: List[Dict[str, object]]):
    file_path = tmp_path / "tasks.json"
    storage_manager = storage.create_storage(str(file_path))
    for entry in tasks:
        storage.save_task(storage_manager, entry)
    return storage_manager


def create_manager_with_storage(storage_manager, client=None):
    mcp_client = client if client is not None else create_dummy_mcp_client()
    manager = job_manager.create_job_manager(mcp_client, storage_manager)
    return manager


def test_list_tasks_returns_all_tasks(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    tasks.append(create_serialized_task("task-1", "pending"))
    tasks.append(create_serialized_task("task-2", "completed"))
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    result = job_manager.list_tasks(manager)
    assert len(result) == 2
    found_ids: List[str] = []
    for item in result:
        found_ids.append(item["id"])
    assert "task-1" in found_ids
    assert "task-2" in found_ids


def test_list_tasks_filters_pending(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    tasks.append(create_serialized_task("task-1", "pending"))
    tasks.append(create_serialized_task("task-2", "in_progress"))
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    result = job_manager.list_tasks(manager, status="pending")
    assert len(result) == 1
    assert result[0]["id"] == "task-1"


def test_list_tasks_filters_in_progress(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    tasks.append(create_serialized_task("task-1", "pending"))
    tasks.append(create_serialized_task("task-2", "in_progress"))
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    result = job_manager.list_tasks(manager, status="in_progress")
    assert len(result) == 1
    assert result[0]["id"] == "task-2"


def test_list_tasks_filters_completed(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    tasks.append(create_serialized_task("task-1", "completed"))
    tasks.append(create_serialized_task("task-2", "in_progress"))
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    result = job_manager.list_tasks(manager, status="completed")
    assert len(result) == 1
    assert result[0]["id"] == "task-1"


def test_list_tasks_returns_empty_list_for_no_tasks(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    result = job_manager.list_tasks(manager)
    assert result == []


def test_list_tasks_uses_storage_data(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    tasks.append(create_serialized_task("task-1", "pending"))
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    new_task = create_serialized_task("task-2", "pending")
    storage.save_task(storage_manager, new_task)
    result = job_manager.list_tasks(manager)
    assert len(result) == 2


def test_list_tasks_returns_normalized_jules_tasks(tmp_path) -> None:
    tasks: List[Dict[str, object]] = []
    tasks.append(create_serialized_task("task-1", "pending"))
    storage_manager = create_storage_manager_with_tasks(tmp_path, tasks)
    manager = create_manager_with_storage(storage_manager)
    result = job_manager.list_tasks(manager)
    assert len(result) == 1
    task = result[0]
    assert isinstance(task["created_at"], datetime)
    assert isinstance(task["updated_at"], datetime)


def test_get_task_invokes_mcp_tool(tmp_path) -> None:
    raw_task = create_serialized_task("task-10", "pending")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps(raw_task)
        response = {"content": [{"type": "text", "text": payload}]}
        return response

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.get_task(manager, "task-10")
    assert result["id"] == "task-10"
    assert len(stub_client["calls"]) == 1
    call = stub_client["calls"][0]
    assert call["name"] == "jules_get_task"
    assert call["arguments"] == {"taskId": "task-10"}


def test_get_task_updates_storage(tmp_path) -> None:
    raw_task = create_serialized_task("task-11", "completed")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps(raw_task)
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    job_manager.get_task(manager, "task-11")
    saved = storage.get_task(storage_manager, "task-11")
    assert saved["status"] == "completed"


def test_get_task_handles_not_found(tmp_path) -> None:

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"error": "not_found"})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(KeyError):
        job_manager.get_task(manager, "missing-id")


def test_get_task_validates_identifier(tmp_path) -> None:
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.get_task(manager, " ")


def test_get_task_rejects_invalid_identifier_format(tmp_path) -> None:
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.get_task(manager, "bad id")


def test_get_task_handles_mcp_errors(tmp_path) -> None:

    def responder(name: str, arguments: Dict[str, object]):
        raise RuntimeError("mcp failure")

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(RuntimeError):
        job_manager.get_task(manager, "task-12")


def test_get_task_requires_valid_response(tmp_path) -> None:

    def responder(name: str, arguments: Dict[str, object]):
        return {"content": [{"type": "text", "text": "not-json"}]}

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(ValueError):
        job_manager.get_task(manager, "task-13")


def test_create_task_invokes_mcp_tool(tmp_path) -> None:
    raw_task = create_serialized_task("task-20", "pending")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps(raw_task)
        response = {"content": [{"type": "text", "text": payload}]}
        return response

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.create_task(manager, "Example task", "owner/repo", branch="dev")
    assert result["id"] == "task-20"
    assert len(stub_client["calls"]) == 1
    call = stub_client["calls"][0]
    assert call["name"] == "jules_create_task"
    assert call["arguments"] == {
        "description": "Example task",
        "repository": "owner/repo",
        "branch": "dev",
    }


def test_create_task_defaults_branch(tmp_path) -> None:
    raw_task = create_serialized_task("task-21", "pending")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps(raw_task)
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    job_manager.create_task(manager, "Example", "owner/repo")
    call = stub_client["calls"][0]
    assert call["arguments"]["branch"] == "main"


def test_create_task_updates_storage(tmp_path) -> None:
    raw_task = create_serialized_task("task-22", "in_progress")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps(raw_task)
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    job_manager.create_task(manager, "Example", "owner/repo")
    saved = storage.get_task(storage_manager, "task-22")
    assert saved["status"] == "in_progress"


def test_create_task_validates_inputs(tmp_path) -> None:
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.create_task(manager, "", "owner/repo")
    with pytest.raises(ValueError):
        job_manager.create_task(manager, "Example", " ")


def test_create_task_handles_mcp_failure(tmp_path) -> None:

    def responder(name: str, arguments: Dict[str, object]):
        raise RuntimeError("mcp failure")

    stub_client = create_stub_mcp_client(responder)
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(RuntimeError):
        job_manager.create_task(manager, "Example", "owner/repo")


def create_storage_with_existing_task(tmp_path, task_id="task-30"):
    task = create_serialized_task(task_id, "in_progress")
    storage_manager = create_storage_manager_with_tasks(tmp_path, [task])
    return storage_manager


def test_send_message_invokes_mcp_tool(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-30")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": True})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.send_message(manager, "task-30", "Hello Jules")
    assert result
    assert len(stub_client["calls"]) == 1
    call = stub_client["calls"][0]
    assert call["name"] == "jules_send_message"
    assert call["arguments"] == {"taskId": "task-30", "message": "Hello Jules"}


def test_send_message_updates_chat_history(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-31")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": True})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    job_manager.send_message(manager, "task-31", "Progress update")
    stored = storage.get_task(storage_manager, "task-31")
    history = stored.get("chat_history", [])
    assert len(history) == 1
    last = history[-1]
    assert last["type"] == "user"
    assert last["content"] == "Progress update"


def test_send_message_validates_task_identifier(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-32")
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.send_message(manager, " ", "Hello")


def test_send_message_validates_message(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-33")
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.send_message(manager, "task-33", " ")


def test_send_message_requires_existing_task(tmp_path) -> None:
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(KeyError):
        job_manager.send_message(manager, "missing", "Hello")


def test_send_message_handles_failure_response(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-34")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": False, "error": "not sent"})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.send_message(manager, "task-34", "Hello")
    assert result is False


def test_send_message_handles_mcp_exception(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-35")

    def responder(name: str, arguments: Dict[str, object]):
        raise RuntimeError("transport error")

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(RuntimeError):
        job_manager.send_message(manager, "task-35", "Hello")


def test_send_message_requires_valid_response(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-36")

    def responder(name: str, arguments: Dict[str, object]):
        return {"content": [{"type": "text", "text": "not-json"}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(ValueError):
        job_manager.send_message(manager, "task-36", "Hello")


def test_send_message_handles_error_payload(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-37")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"error": "delivery_failed"})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(RuntimeError):
        job_manager.send_message(manager, "task-37", "Hello")
