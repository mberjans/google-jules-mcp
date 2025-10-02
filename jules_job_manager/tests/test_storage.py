from pathlib import Path
from typing import Dict

import pytest

from src import storage


def create_sample_task(task_id: str, status: str = "pending") -> Dict[str, object]:
    created_at = "2025-01-02T12:00:00+00:00"
    updated_at = created_at
    task = {
        "id": task_id,
        "title": "Example",
        "description": "Details",
        "repository": "owner/repo",
        "branch": "main",
        "status": status,
        "created_at": created_at,
        "updated_at": updated_at,
        "url": "https://example.com/task",
        "chat_history": [],
        "source_files": [],
    }
    return task


@pytest.fixture()
def temp_storage(tmp_path: Path):
    tasks_file = tmp_path / "tasks.json"
    manager = storage.create_storage(str(tasks_file))
    return manager, tasks_file


def test_storage_initialization_creates_file(temp_storage):
    manager, tasks_file = temp_storage
    assert tasks_file.exists()
    assert storage.storage_path(manager) == str(tasks_file)


def test_save_and_get_task_roundtrip(temp_storage):
    manager, tasks_file = temp_storage
    task = create_sample_task("task-1")
    storage.save_task(manager, task)
    saved = storage.get_task(manager, "task-1")
    assert saved["id"] == "task-1"
    assert saved["status"] == "pending"
    tasks = storage.list_tasks(manager)
    assert len(tasks) == 1
    assert tasks[0]["id"] == "task-1"


def test_save_task_overwrites_existing(temp_storage):
    manager, _ = temp_storage
    first = create_sample_task("task-2", "pending")
    second = create_sample_task("task-2", "completed")
    storage.save_task(manager, first)
    storage.save_task(manager, second)
    retrieved = storage.get_task(manager, "task-2")
    assert retrieved["status"] == "completed"


def test_list_tasks_filters_by_status(temp_storage):
    manager, _ = temp_storage
    storage.save_task(manager, create_sample_task("task-3", "pending"))
    storage.save_task(manager, create_sample_task("task-4", "completed"))
    pending = storage.list_tasks(manager, status="pending")
    assert len(pending) == 1
    assert pending[0]["id"] == "task-3"
    completed = storage.list_tasks(manager, status="completed")
    assert len(completed) == 1
    assert completed[0]["id"] == "task-4"


def test_delete_task_removes_entry(temp_storage):
    manager, _ = temp_storage
    storage.save_task(manager, create_sample_task("task-5"))
    storage.delete_task(manager, "task-5")
    with pytest.raises(KeyError):
        storage.get_task(manager, "task-5")


def test_persistence_across_instances(tmp_path: Path):
    tasks_file = tmp_path / "tasks.json"
    manager_a = storage.create_storage(str(tasks_file))
    storage.save_task(manager_a, create_sample_task("task-6"))
    manager_b = storage.create_storage(str(tasks_file))
    retrieved = storage.get_task(manager_b, "task-6")
    assert retrieved["id"] == "task-6"


def test_missing_task_raises_key_error(temp_storage):
    manager, _ = temp_storage
    with pytest.raises(KeyError):
        storage.get_task(manager, "missing")


def test_corrupt_file_resets_to_empty(tmp_path: Path):
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text("not json", encoding="utf-8")
    manager = storage.create_storage(str(tasks_file))
    assert storage.list_tasks(manager) == []


def test_concurrent_access_uses_lock(tmp_path: Path):
    tasks_file = tmp_path / "tasks.json"
    manager = storage.create_storage(str(tasks_file))
    other = storage.create_storage(str(tasks_file))
    storage.save_task(manager, create_sample_task("task-7"))
    result = storage.list_tasks(other)
    assert len(result) == 1
    assert result[0]["id"] == "task-7"
    assert result[0]["status"] == "pending"
