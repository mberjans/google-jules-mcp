"""Functional Job Manager helpers."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from src import models, storage


LOGGER = logging.getLogger(__name__)


def _validate_required_dependency(name: str, value: Any) -> Any:
    """Ensure a dependency value is provided.

    Args:
        name: Dependency label used in error messages.
        value: Injected object to validate.

    Returns:
        The original dependency when it is present.

    Raises:
        ValueError: If the dependency is missing.
    """
    if value is None:
        message = f"{name} dependency is required"
        raise ValueError(message)
    return value


def _ensure_callable(attribute_name: str, provider: Any) -> None:
    """Verify that the provider exposes a callable with the requested name.

    Args:
        attribute_name: Name of the callable attribute to inspect.
        provider: Dependency that should expose the callable.

    Raises:
        TypeError: If the callable attribute is not available.
    """
    candidate = getattr(provider, attribute_name, None)
    if callable(candidate):
        return
    if isinstance(provider, dict):
        if attribute_name in provider and callable(provider[attribute_name]):
            return
    message = f"Expected '{attribute_name}' callable on dependency"
    raise TypeError(message)


def create_job_manager(mcp_client: Any, storage: Any) -> Dict[str, Any]:
    """Create a job manager record holding validated dependencies.

    Args:
        mcp_client: Object capable of invoking MCP tools via ``invoke_tool``.
        storage: Storage manager responsible for persistence operations.

    Returns:
        A dictionary with ``mcp_client`` and ``storage`` keys referencing the
        validated dependencies.

    Raises:
        ValueError: When either dependency is missing.
        TypeError: When the MCP client cannot invoke tools.
    """
    validated_client = _validate_required_dependency("mcp_client", mcp_client)
    validated_storage = _validate_required_dependency("storage", storage)
    _ensure_callable("invoke_tool", validated_client)
    manager: Dict[str, Any] = {}
    manager["mcp_client"] = validated_client
    manager["storage"] = validated_storage
    return manager


def list_tasks(manager: Dict[str, Any], status: Optional[str] = None) -> List[Dict[str, object]]:
    """Return normalized task dictionaries from the storage backend.

    Args:
        manager: Job manager dictionary created by ``create_job_manager``.
        status: Optional status filter passed to storage.

    Returns:
        A list of task dictionaries normalized via ``models.jules_task_from_dict``.
    """
    storage_manager = manager.get("storage")
    if storage_manager is None:
        raise ValueError("Storage manager is missing")
    LOGGER.info("Listing tasks", extra={"status": status})
    raw_tasks = storage.list_tasks(storage_manager, status)
    normalized: List[Dict[str, object]] = []
    for entry in raw_tasks:
        normalized.append(models.jules_task_from_dict(entry))
    return normalized


def _validate_task_identifier(task_id: str) -> str:
    """Ensure the provided task identifier is non-empty and well-formed."""
    if task_id is None:
        raise ValueError("Task identifier is required")
    stripped = task_id.strip()
    if not stripped:
        raise ValueError("Task identifier cannot be blank")
    allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    for character in stripped:
        if character not in allowed_characters:
            raise ValueError("Task identifier contains invalid characters")
    return stripped


def _extract_response_text(response: Dict[str, object]) -> str:
    content = response.get("content")
    if not isinstance(content, list):
        raise ValueError("Response content missing")
    for item in content:
        if not isinstance(item, dict):
            continue
        text_value = item.get("text")
        if isinstance(text_value, str) and text_value.strip():
            return text_value
    raise ValueError("Response content did not include text payload")


def _invoke_mcp_tool(mcp_client: Any, name: str, arguments: Dict[str, object]) -> Dict[str, object]:
    """Invoke an MCP tool regardless of client representation."""
    handler = getattr(mcp_client, "invoke_tool", None)
    if callable(handler):
        return handler(name, arguments)
    if isinstance(mcp_client, dict):
        candidate = mcp_client.get("invoke_tool")
        if callable(candidate):
            return candidate(name, arguments)
    raise ValueError("MCP client cannot invoke tools")


def get_task(manager: Dict[str, Any], task_id: str) -> Dict[str, object]:
    """Fetch task details from the MCP server and persist them locally.

    Args:
        manager: Job manager dictionary produced by ``create_job_manager``.
        task_id: Identifier of the task to retrieve.

    Returns:
        Normalized Jules task dictionary.

    Raises:
        ValueError: When dependencies, identifiers, or payloads are invalid.
        KeyError: If the task cannot be found by the MCP server.
        RuntimeError: When MCP invocation fails.
    """
    validated_id = _validate_task_identifier(task_id)
    mcp_client = manager.get("mcp_client")
    if mcp_client is None:
        raise ValueError("MCP client is missing")
    storage_manager = manager.get("storage")
    if storage_manager is None:
        raise ValueError("Storage manager is missing")
    LOGGER.info("Fetching task from MCP", extra={"task_id": validated_id})
    try:
        response = _invoke_mcp_tool(mcp_client, "jules_get_task", {"taskId": validated_id})
    except Exception as error:  # noqa: BLE001
        LOGGER.error("MCP invocation failed", extra={"task_id": validated_id})
        raise RuntimeError("Failed to fetch task from MCP") from error
    text_payload = _extract_response_text(response)
    try:
        raw_data = json.loads(text_payload)
    except json.JSONDecodeError as error:
        raise ValueError("Unable to parse task payload") from error
    if isinstance(raw_data, dict) and raw_data.get("error") == "not_found":
        raise KeyError(f"Task '{validated_id}' not found")
    if not isinstance(raw_data, dict):
        raise ValueError("Task payload must be a dictionary")
    normalized_task = models.jules_task_from_dict(raw_data)
    serialized_task = models.jules_task_to_dict(normalized_task)
    storage.save_task(storage_manager, serialized_task)
    return normalized_task
