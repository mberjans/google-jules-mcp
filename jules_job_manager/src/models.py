"""Functional data model helpers for Jules Job Manager."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Dict, Iterable, List, Optional

TASK_STATUS_VALUES: List[str] = [
    "pending",
    "in_progress",
    "completed",
    "paused",
    "waiting_approval",
]

CHAT_ROLES: List[str] = ["user", "jules", "system"]


def get_task_status_values() -> List[str]:
    """Return all allowed task status values."""
    return list(TASK_STATUS_VALUES)


def validate_task_status(status: str) -> None:
    """Ensure the provided status string is valid."""
    if status not in TASK_STATUS_VALUES:
        message = f"Unsupported task status: {status}"
        raise ValueError(message)


def _ensure_timestamp(timestamp: Optional[str]) -> str:
    if timestamp is None:
        now = datetime.now().astimezone()
        return now.isoformat()
    datetime.fromisoformat(timestamp)
    return timestamp


def create_chat_message(role: str, content: str, timestamp: Optional[str] = None) -> Dict[str, str]:
    """Create a chat message dictionary with validated data."""
    if role not in CHAT_ROLES:
        message = f"Unsupported chat role: {role}"
        raise ValueError(message)
    if not content:
        raise ValueError("Chat message content cannot be empty")
    resolved_timestamp = _ensure_timestamp(timestamp)
    message_dict: Dict[str, str] = {
        "type": role,
        "content": content,
        "timestamp": resolved_timestamp,
    }
    return message_dict


def chat_message_to_dict(message: Dict[str, str]) -> Dict[str, str]:
    """Return a shallow copy of a chat message dictionary for serialization."""
    return dict(message)


def chat_message_from_dict(data: Dict[str, str]) -> Dict[str, str]:
    """Validate and return a chat message dictionary from raw data."""
    role = data.get("type")
    content = data.get("content")
    timestamp = data.get("timestamp")
    return create_chat_message(role, content, timestamp)


def create_source_file(
    filename: str,
    url: str,
    status: str,
    diff: Optional[str] = None,
) -> Dict[str, Optional[str]]:
    """Create a source file dictionary containing metadata."""
    if not filename:
        raise ValueError("Source file filename cannot be empty")
    if not url:
        raise ValueError("Source file URL cannot be empty")
    if not status:
        raise ValueError("Source file status cannot be empty")
    file_dict: Dict[str, Optional[str]] = {
        "filename": filename,
        "url": url,
        "status": status,
        "diff": diff,
    }
    return file_dict


def source_file_to_dict(file_dict: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """Return a shallow copy of a source file dictionary for serialization."""
    return dict(file_dict)


def source_file_from_dict(data: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """Validate and return a source file dictionary from raw data."""
    filename = data.get("filename")
    url = data.get("url")
    status = data.get("status")
    diff = data.get("diff")
    return create_source_file(filename, url, status, diff)


def _ensure_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        message = "Expected datetime instance"
        raise TypeError(message)
    if value.tzinfo is None:
        return value.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return value


def _normalize_chat_history(history: Optional[Iterable[Dict[str, str]]]) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    if history is None:
        return normalized
    for item in history:
        normalized.append(chat_message_from_dict(item))
    return normalized


def _normalize_source_files(files: Optional[Iterable[Dict[str, Optional[str]]]]) -> List[Dict[str, Optional[str]]]:
    normalized: List[Dict[str, Optional[str]]] = []
    if files is None:
        return normalized
    for item in files:
        normalized.append(source_file_from_dict(item))
    return normalized


def create_jules_task(
    task_id: str,
    title: str,
    description: str,
    repository: str,
    branch: str,
    status: str,
    created_at: datetime,
    updated_at: datetime,
    url: str,
    chat_history: Optional[Iterable[Dict[str, str]]] = None,
    source_files: Optional[Iterable[Dict[str, Optional[str]]]] = None,
) -> Dict[str, object]:
    """Create a Jules task dictionary with validated contents."""
    if not task_id:
        raise ValueError("Task identifier cannot be empty")
    if not title:
        raise ValueError("Task title cannot be empty")
    if not repository:
        raise ValueError("Repository cannot be empty")
    if not branch:
        raise ValueError("Branch cannot be empty")
    if not url:
        raise ValueError("Task URL cannot be empty")
    validate_task_status(status)
    normalized_created = _ensure_datetime(created_at)
    normalized_updated = _ensure_datetime(updated_at)
    normalized_history = _normalize_chat_history(chat_history)
    normalized_files = _normalize_source_files(source_files)
    task_dict: Dict[str, object] = {
        "id": task_id,
        "title": title,
        "description": description,
        "repository": repository,
        "branch": branch,
        "status": status,
        "created_at": normalized_created,
        "updated_at": normalized_updated,
        "url": url,
        "chat_history": normalized_history,
        "source_files": normalized_files,
    }
    return task_dict


def jules_task_to_dict(task: Dict[str, object]) -> Dict[str, object]:
    """Convert an in-memory task dictionary to a JSON-serializable dict."""
    serialized: Dict[str, object] = {}
    for key, value in task.items():
        serialized[key] = value
    created_at = serialized.get("created_at")
    updated_at = serialized.get("updated_at")
    if isinstance(created_at, datetime):
        serialized["created_at"] = created_at.isoformat()
    if isinstance(updated_at, datetime):
        serialized["updated_at"] = updated_at.isoformat()
    history = serialized.get("chat_history", [])
    new_history: List[Dict[str, str]] = []
    for item in history:
        new_history.append(chat_message_to_dict(item))
    serialized["chat_history"] = new_history
    files = serialized.get("source_files", [])
    new_files: List[Dict[str, Optional[str]]] = []
    for item in files:
        new_files.append(source_file_to_dict(item))
    serialized["source_files"] = new_files
    return serialized


def jules_task_from_dict(data: Dict[str, object]) -> Dict[str, object]:
    """Create a task dictionary from serialized data."""
    status = data.get("status")
    created_at_value = data.get("created_at")
    updated_at_value = data.get("updated_at")
    if not isinstance(created_at_value, datetime):
        created_at_value = datetime.fromisoformat(str(created_at_value))
    if not isinstance(updated_at_value, datetime):
        updated_at_value = datetime.fromisoformat(str(updated_at_value))
    chat_history_input = data.get("chat_history")
    source_files_input = data.get("source_files")
    return create_jules_task(
        str(data.get("id")),
        str(data.get("title")),
        str(data.get("description")),
        str(data.get("repository")),
        str(data.get("branch")),
        str(status),
        created_at_value,
        updated_at_value,
        str(data.get("url")),
        chat_history_input,
        source_files_input,
    )


def clone_jules_task(task: Dict[str, object]) -> Dict[str, object]:
    """Return a deep copy of a task dictionary."""
    return deepcopy(task)
