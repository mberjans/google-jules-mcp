"""Functional helpers for task storage and retrieval."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


def _ensure_parent_directory(file_path: str) -> None:
    """Create parent directories for the storage file if missing."""
    path = Path(file_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def _load_raw_data(file_path: str) -> Dict[str, Dict[str, object]]:
    """Load all task data from disk, returning an empty dict on failure."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            contents = handle.read().strip()
            if not contents:
                return {}
            data = json.loads(contents)
            if not isinstance(data, dict):
                return {}
            return {str(key): value for key, value in data.items() if isinstance(value, dict)}
    except json.JSONDecodeError:
        return {}


def _serialize_data(data: Dict[str, Dict[str, object]]) -> str:
    """Serialize task data to a normalized JSON string."""
    return json.dumps(data, indent=2, sort_keys=True)


def _save_raw_data(file_path: str, data: Dict[str, Dict[str, object]], serialized: str) -> None:
    """Persist task data to disk with stable formatting using atomic replace."""
    _ensure_parent_directory(file_path)
    temp_path = Path(file_path).with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as handle:
        handle.write(serialized)
    os.replace(temp_path, file_path)


def _copy_dict_of_dicts(data: Dict[str, Dict[str, object]]) -> Dict[str, Dict[str, object]]:
    """Return a deep-ish copy of a nested dictionary without comprehensions."""
    cloned: Dict[str, Dict[str, object]] = {}
    for key, value in data.items():
        inner: Dict[str, object] = {}
        for inner_key, inner_value in value.items():
            inner[inner_key] = inner_value
        cloned[str(key)] = inner
    return cloned


def create_storage(file_path: str) -> Dict[str, object]:
    """Create a storage manager backed by the provided JSON file."""
    _ensure_parent_directory(file_path)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write("{}")
    manager = {
        "file_path": file_path,
        "lock": Path(file_path).with_suffix(".lock"),
        "cache": None,
        "cache_mtime": None,
        "cache_serialized": None,
    }
    return manager


def storage_path(manager: Dict[str, object]) -> str:
    """Return the file path associated with the storage manager."""
    return str(manager["file_path"])


def _acquire_lock(manager: Dict[str, object]) -> None:
    """Create a simple lock file to coordinate writes."""
    lock_file = manager["lock"]
    if Path(lock_file).exists():
        return
    Path(lock_file).touch()


def _release_lock(manager: Dict[str, object]) -> None:
    """Remove the lock file if it exists."""
    lock_file = manager["lock"]
    path = Path(lock_file)
    if path.exists():
        path.unlink()


def _load_all(manager: Dict[str, object]) -> Dict[str, Dict[str, object]]:
    """Load all tasks from the manager's backing file."""
    file_path = storage_path(manager)
    current_mtime = None
    if os.path.exists(file_path):
        current_mtime = os.path.getmtime(file_path)
    cached_data = manager.get("cache")
    cached_mtime = manager.get("cache_mtime")
    if cached_data is not None and cached_mtime == current_mtime:
        return _copy_dict_of_dicts(cached_data)
    data = _load_raw_data(file_path)
    serialized = _serialize_data(data)
    manager["cache"] = _copy_dict_of_dicts(data)
    manager["cache_mtime"] = current_mtime
    manager["cache_serialized"] = serialized
    return _copy_dict_of_dicts(data)


def _save_all(manager: Dict[str, object], data: Dict[str, Dict[str, object]]) -> None:
    """Save all tasks to the manager's backing file."""
    file_path = storage_path(manager)
    serialized = _serialize_data(data)
    cached_serialized = manager.get("cache_serialized")
    if cached_serialized is not None and cached_serialized == serialized:
        manager["cache"] = _copy_dict_of_dicts(data)
        return
    existing = manager.get("cache")
    if existing is not None:
        same = True
        for key, value in data.items():
            if key not in existing or value != existing[key]:
                same = False
                break
        if same and len(existing) == len(data):
            manager["cache"] = _copy_dict_of_dicts(data)
            manager["cache_serialized"] = serialized
            return
    _save_raw_data(file_path, data, serialized)
    manager["cache"] = _copy_dict_of_dicts(data)
    manager["cache_serialized"] = serialized
    if os.path.exists(file_path):
        manager["cache_mtime"] = os.path.getmtime(file_path)


def save_task(manager: Dict[str, object], task: Dict[str, object]) -> None:
    """Insert or update a task entry on disk."""
    _acquire_lock(manager)
    try:
        tasks = _load_all(manager)
        tasks[str(task["id"])] = task
        _save_all(manager, tasks)
    finally:
        _release_lock(manager)


def get_task(manager: Dict[str, object], task_id: str) -> Dict[str, object]:
    """Return a task by identifier, raising KeyError when missing."""
    tasks = _load_all(manager)
    key = str(task_id)
    if key not in tasks:
        raise KeyError(f"Task '{task_id}' not found")
    return tasks[key]


def list_tasks(manager: Dict[str, object], status: Optional[str] = None) -> List[Dict[str, object]]:
    """Return all tasks, optionally filtered by status and sorted by creation time."""
    tasks = _load_all(manager)
    results = list(tasks.values())
    if status is not None:
        filtered: List[Dict[str, object]] = []
        for entry in results:
            if entry.get("status") == status:
                filtered.append(entry)
        results = filtered
    results.sort(key=lambda task: task.get("created_at", ""))
    return results


def delete_task(manager: Dict[str, object], task_id: str) -> None:
    """Remove a task from the backing store, raising KeyError when missing."""
    _acquire_lock(manager)
    try:
        tasks = _load_all(manager)
        key = str(task_id)
        if key not in tasks:
            raise KeyError(f"Task '{task_id}' not found")
        del tasks[key]
        _save_all(manager, tasks)
    finally:
        _release_lock(manager)
