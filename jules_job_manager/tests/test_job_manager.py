"""Tests for Job Manager initialization logic."""

import json
from datetime import datetime
from types import SimpleNamespace
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


def create_storage_with_existing_task(tmp_path, task_id="task-30", status="in_progress"):
    task = create_serialized_task(task_id, status)
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


def test_approve_plan_invokes_mcp_tool(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-40", status="waiting_approval")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": True})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.approve_plan(manager, "task-40")
    assert result is True
    assert len(stub_client["calls"]) == 1
    call = stub_client["calls"][0]
    assert call["name"] == "jules_approve_plan"
    assert call["arguments"] == {"taskId": "task-40"}


def test_approve_plan_updates_status(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-41", status="waiting_approval")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": True})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    job_manager.approve_plan(manager, "task-41")
    stored = storage.get_task(storage_manager, "task-41")
    assert stored["status"] == "in_progress"


def test_approve_plan_requires_waiting_status(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-42", status="pending")
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.approve_plan(manager, "task-42")


def test_approve_plan_handles_failure_response(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-43", status="waiting_approval")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": False})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.approve_plan(manager, "task-43")
    assert result is False
    stored = storage.get_task(storage_manager, "task-43")
    assert stored["status"] == "waiting_approval"


def test_approve_plan_handles_error_payload(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-44", status="waiting_approval")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"error": "approval_failed"})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(RuntimeError):
        job_manager.approve_plan(manager, "task-44")


def test_approve_plan_validates_task_identifier(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-45", status="waiting_approval")
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.approve_plan(manager, " ")


def test_approve_plan_requires_existing_task(tmp_path) -> None:
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(KeyError):
        job_manager.approve_plan(manager, "missing")


def test_approve_plan_requires_valid_response(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-46", status="waiting_approval")

    def responder(name: str, arguments: Dict[str, object]):
        return {"content": [{"type": "text", "text": "not-json"}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(ValueError):
        job_manager.approve_plan(manager, "task-46")


def test_resume_task_invokes_mcp_tool(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-50", status="paused")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": True})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.resume_task(manager, "task-50")
    assert result is True
    assert len(stub_client["calls"]) == 1
    call = stub_client["calls"][0]
    assert call["name"] == "jules_resume_task"
    assert call["arguments"] == {"taskId": "task-50"}


def test_resume_task_updates_status(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-51", status="paused")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": True})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    job_manager.resume_task(manager, "task-51")
    stored = storage.get_task(storage_manager, "task-51")
    assert stored["status"] == "in_progress"


def test_resume_task_requires_paused_status(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-52", status="pending")
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.resume_task(manager, "task-52")


def test_resume_task_handles_failure_response(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-53", status="paused")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"success": False})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    result = job_manager.resume_task(manager, "task-53")
    assert result is False
    stored = storage.get_task(storage_manager, "task-53")
    assert stored["status"] == "paused"


def test_resume_task_handles_error_payload(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-54", status="paused")

    def responder(name: str, arguments: Dict[str, object]):
        payload = json.dumps({"error": "resume_failed"})
        return {"content": [{"type": "text", "text": payload}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(RuntimeError):
        job_manager.resume_task(manager, "task-54")


def test_resume_task_validates_task_identifier(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-55", status="paused")
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(ValueError):
        job_manager.resume_task(manager, " ")


def test_resume_task_requires_existing_task(tmp_path) -> None:
    storage_manager = create_storage_manager_with_tasks(tmp_path, [])
    manager = create_manager_with_storage(storage_manager)
    with pytest.raises(KeyError):
        job_manager.resume_task(manager, "missing")


def test_resume_task_requires_valid_response(tmp_path) -> None:
    storage_manager = create_storage_with_existing_task(tmp_path, "task-56", status="paused")

    def responder(name: str, arguments: Dict[str, object]):
        return {"content": [{"type": "text", "text": "not-json"}]}

    stub_client = create_stub_mcp_client(responder)
    manager = create_manager_with_storage(storage_manager, stub_client)
    with pytest.raises(ValueError):
        job_manager.resume_task(manager, "task-56")


def test_monitor_task_polls_until_completed(monkeypatch) -> None:
    statuses: list = []
    statuses.append("pending")
    statuses.append("in_progress")
    statuses.append("completed")
    calls: list = []

    def fake_get_task(manager, task_identifier):
        calls.append(task_identifier)
        if statuses:
            current_status = statuses.pop(0)
        else:
            current_status = "completed"
        timestamp = datetime.now().astimezone()
        task = models.create_jules_task(
            task_identifier,
            "Sample Title",
            "Sample Description",
            "owner/repo",
            "main",
            current_status,
            timestamp,
            timestamp,
            "https://example.com/task",
        )
        return task

    sleeps: list = []

    def fake_sleep(interval):
        sleeps.append(interval)

    messages: list = []

    def create_console_stub():
        def record_message(message):
            messages.append(message)

        console = SimpleNamespace(print=record_message)
        return console

    original_manager = job_manager.create_job_manager(create_dummy_mcp_client(), create_dummy_storage())
    monkeypatch.setattr(job_manager, "get_task", fake_get_task)
    monkeypatch.setattr(job_manager, "_sleep", fake_sleep)
    monkeypatch.setattr(job_manager, "_create_console", create_console_stub)
    job_manager.monitor_task(original_manager, "task-200", interval=2)
    assert len(calls) == 3
    assert len(sleeps) == 2
    assert sleeps[0] == 2
    assert sleeps[1] == 2
    assert messages
    last_index = len(messages) - 1
    assert "completed" in str(messages[last_index])


def test_monitor_task_handles_keyboard_interrupt(monkeypatch) -> None:
    call_counter: dict = {"count": 0}

    def fake_get_task(manager, task_identifier):
        call_counter["count"] = call_counter["count"] + 1
        timestamp = datetime.now().astimezone()
        task = models.create_jules_task(
            task_identifier,
            "Sample Title",
            "Sample Description",
            "owner/repo",
            "main",
            "in_progress",
            timestamp,
            timestamp,
            "https://example.com/task",
        )
        return task

    def fake_sleep(interval):
        raise KeyboardInterrupt()

    messages: list = []

    def create_console_stub():
        def record_message(message):
            messages.append(message)

        console = SimpleNamespace(print=record_message)
        return console

    original_manager = job_manager.create_job_manager(create_dummy_mcp_client(), create_dummy_storage())
    monkeypatch.setattr(job_manager, "get_task", fake_get_task)
    monkeypatch.setattr(job_manager, "_sleep", fake_sleep)
    monkeypatch.setattr(job_manager, "_create_console", create_console_stub)
    job_manager.monitor_task(original_manager, "task-201", interval=3)
    assert call_counter["count"] == 1
    assert messages
    last_index = len(messages) - 1
    assert "Monitoring stopped" in str(messages[last_index])


def test_monitor_task_raises_for_missing_task(monkeypatch) -> None:
    def fake_get_task(manager, task_identifier):
        raise KeyError("missing")

    def fake_sleep(interval):
        return None

    def create_console_stub():
        def record_message(message):
            return None

        console = SimpleNamespace(print=record_message)
        return console

    original_manager = job_manager.create_job_manager(create_dummy_mcp_client(), create_dummy_storage())
    monkeypatch.setattr(job_manager, "get_task", fake_get_task)
    monkeypatch.setattr(job_manager, "_sleep", fake_sleep)
    monkeypatch.setattr(job_manager, "_create_console", create_console_stub)
    with pytest.raises(KeyError):
        job_manager.monitor_task(original_manager, "task-202", interval=4)
