"""Functional Job Manager helpers."""

from __future__ import annotations

from typing import Any, Dict


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
