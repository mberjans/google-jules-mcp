"""Tests for Job Manager initialization logic."""

import pytest

from src import job_manager


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
