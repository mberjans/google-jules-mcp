from datetime import datetime, timezone

from src import models


def test_task_status_members():
    statuses = models.get_task_status_values()
    expected = {"pending", "in_progress", "completed", "paused", "waiting_approval"}
    assert set(statuses) == expected
    assert len(statuses) == len(expected)


def test_chat_message_initialization():
    timestamp = "2025-01-01T12:00:00+00:00"
    message = models.create_chat_message("system", "status", timestamp)
    assert message["type"] == "system"
    assert message["content"] == "status"
    assert message["timestamp"] == timestamp


def test_chat_message_default_timestamp():
    message = models.create_chat_message("user", "hello")
    parsed = datetime.fromisoformat(message["timestamp"])
    now = datetime.now(timezone.utc)
    delta = now - parsed
    assert abs(delta.total_seconds()) < 10


def test_chat_message_serialization_roundtrip():
    timestamp = "2025-01-01T12:00:00+00:00"
    original = models.create_chat_message("jules", "ready", timestamp)
    data = models.chat_message_to_dict(original)
    assert data["type"] == "jules"
    assert data["content"] == "ready"
    assert data["timestamp"] == timestamp
    restored = models.chat_message_from_dict(data)
    assert restored == original


def test_source_file_initialization():
    source = models.create_source_file("README.md", "https://example.com/README.md", "modified")
    assert source["filename"] == "README.md"
    assert source["url"] == "https://example.com/README.md"
    assert source["status"] == "modified"
    assert source["diff"] is None


def test_source_file_optional_diff():
    source = models.create_source_file("src/module.py", "https://example.com/src/module.py", "created", "+ new content")
    assert source["diff"] == "+ new content"


def test_source_file_serialization_roundtrip():
    original = models.create_source_file("src/module.py", "https://example.com/src/module.py", "deleted", "- old content")
    data = models.source_file_to_dict(original)
    assert data["filename"] == "src/module.py"
    assert data["url"] == "https://example.com/src/module.py"
    assert data["status"] == "deleted"
    assert data["diff"] == "- old content"
    restored = models.source_file_from_dict(data)
    assert restored == original


def test_jules_task_initialization():
    created_at = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
    updated_at = datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc)
    task = models.create_jules_task(
        "task-123",
        "Sample Task",
        "Do something",
        "owner/repo",
        "main",
        "in_progress",
        created_at,
        updated_at,
        "https://example.com",
    )
    assert task["id"] == "task-123"
    assert task["status"] == "in_progress"
    assert task["chat_history"] == []
    assert task["source_files"] == []


def test_jules_task_optional_lists_default():
    created_at = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
    updated_at = datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc)
    task = models.create_jules_task(
        "task-456",
        "Sample",
        "Details",
        "owner/repo",
        "develop",
        "pending",
        created_at,
        updated_at,
        "https://example.com",
    )
    assert task["chat_history"] == []
    assert task["source_files"] == []


def test_jules_task_to_dict_nested_serialization():
    created_at = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
    updated_at = datetime(2025, 1, 1, 13, 0, tzinfo=timezone.utc)
    message = models.create_chat_message("user", "Hello", "2025-01-01T12:05:00+00:00")
    source_file = models.create_source_file("README.md", "https://example.com/README.md", "modified", "- old\n+ new")
    task = models.create_jules_task(
        "task-789",
        "Another Task",
        "Work",
        "owner/repo",
        "main",
        "completed",
        created_at,
        updated_at,
        "https://example.com/task",
        [message],
        [source_file],
    )
    data = models.jules_task_to_dict(task)
    assert data["id"] == "task-789"
    assert data["status"] == "completed"
    assert data["created_at"] == created_at.isoformat()
    assert data["updated_at"] == updated_at.isoformat()
    chat_list = data["chat_history"]
    assert len(chat_list) == 1
    assert chat_list[0]["type"] == "user"
    files_list = data["source_files"]
    assert len(files_list) == 1
    assert files_list[0]["filename"] == "README.md"


def test_jules_task_from_dict_roundtrip():
    chat_dict = {"type": "jules", "content": "Done", "timestamp": "2025-01-01T12:10:00+00:00"}
    file_dict = {"filename": "README.md", "url": "https://example.com/README.md", "status": "modified", "diff": "- old\n+ new"}
    data = {
        "id": "task-101",
        "title": "Finish",
        "description": "Complete the job",
        "repository": "owner/repo",
        "branch": "main",
        "status": "paused",
        "created_at": "2025-01-01T11:00:00+00:00",
        "updated_at": "2025-01-01T11:30:00+00:00",
        "url": "https://example.com/task/101",
        "chat_history": [chat_dict],
        "source_files": [file_dict],
    }
    task = models.jules_task_from_dict(data)
    assert task["id"] == "task-101"
    assert task["status"] == "paused"
    assert task["chat_history"][0]["type"] == "jules"
    restored = models.jules_task_to_dict(task)
    assert restored["id"] == data["id"]


def test_jules_task_to_dict_handles_empty_lists():
    created_at = datetime(2025, 1, 1, 10, 0, tzinfo=timezone.utc)
    updated_at = datetime(2025, 1, 1, 11, 0, tzinfo=timezone.utc)
    task = models.create_jules_task(
        "task-empty",
        "Empty",
        "Empty",
        "owner/repo",
        "main",
        "pending",
        created_at,
        updated_at,
        "https://example.com",
    )
    data = models.jules_task_to_dict(task)
    chat_history = data["chat_history"]
    source_files = data["source_files"]
    assert chat_history == []
    assert source_files == []
