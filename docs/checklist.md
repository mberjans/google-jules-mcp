# Jules Job Manager - Detailed Task Checklist (TDD Approach)

This checklist breaks down each ticket into tiny, testable tasks following Test-Driven Development (TDD) principles.

**TDD Workflow for Each Feature:**
1. Write unit tests first (Red phase)
2. Implement minimal code to pass tests (Green phase)
3. Refactor and improve code quality (Refactor phase)
4. Run tests to verify functionality

---

## Part 1: MVP Tickets (JJM-001 to JJM-025)

### Phase 1: Foundation (Days 1-2)

#### JJM-001: Project Structure Setup
- [x] JJM-001-T01: Create root directory `jules_job_manager/`
- [x] JJM-001-T02: Create `jules_job_manager/src/` directory
- [x] JJM-001-T03: Create `jules_job_manager/tests/` directory
- [x] JJM-001-T04: Create `jules_job_manager/config/` directory
- [x] JJM-001-T05: Create `jules_job_manager/data/` directory
- [x] JJM-001-T06: Create `jules_job_manager/docs/` directory
- [x] JJM-001-T07: Create `jules_job_manager/src/__init__.py`
- [x] JJM-001-T08: Create `jules_job_manager/tests/__init__.py`
- [x] JJM-001-T09: Create `jules_job_manager/requirements.txt` with initial dependencies
- [x] JJM-001-T10: Create `jules_job_manager/setup.py` with package metadata
- [x] JJM-001-T11: Create `jules_job_manager/.gitignore` (if not exists)
- [x] JJM-001-T12: Create `jules_job_manager/README.md` with basic info
- [x] JJM-001-T13: Create `jules_job_manager/config/config.json` with default settings
- [x] JJM-001-T14: Create Python virtual environment: `python -m venv venv`
- [x] JJM-001-T15: Activate virtual environment
- [x] JJM-001-T16: Install dependencies: `pip install -r requirements.txt`
- [x] JJM-001-T17: Verify project structure with `tree` or `ls -R`
- [x] JJM-001-T18: Run `python -m pytest --collect-only` to verify test discovery
- [ ] JJM-001-T19: Commit changes: "JJM-001: Set up project structure"
- [ ] JJM-001-T20: Push to repository

---

#### JJM-002: Data Models Implementation
**TDD: Write tests first, then implement models**

- [x] JJM-002-T01: Create `jules_job_manager/tests/test_models.py`
- [x] JJM-002-T02: Write test for `TaskStatus` enum creation
- [x] JJM-002-T03: Write test for `TaskStatus` enum values (pending, in_progress, completed, paused, failed)
- [x] JJM-002-T04: Write test for `ChatMessage` dataclass initialization
- [x] JJM-002-T05: Write test for `ChatMessage` with all fields (role, content, timestamp)
- [x] JJM-002-T06: Write test for `ChatMessage` default timestamp
- [x] JJM-002-T07: Write test for `SourceFile` dataclass initialization
- [x] JJM-002-T08: Write test for `SourceFile` with all fields (path, status, diff)
- [x] JJM-002-T09: Write test for `JulesTask` dataclass initialization
- [x] JJM-002-T10: Write test for `JulesTask` with all required fields
- [x] JJM-002-T11: Write test for `JulesTask` with optional fields (chat_history, source_files)
- [x] JJM-002-T12: Write test for `JulesTask.to_dict()` method
- [x] JJM-002-T13: Write test for `JulesTask.from_dict()` method
- [x] JJM-002-T14: Write test for nested serialization (ChatMessage, SourceFile in JulesTask)
- [x] JJM-002-T15: Run tests (should fail - Red phase): `pytest tests/test_models.py -v`
- [x] JJM-002-T16: Create `jules_job_manager/src/models.py`
- [x] JJM-002-T17: Implement `TaskStatus` enum with all values
- [x] JJM-002-T18: Implement `ChatMessage` dataclass with type hints
- [x] JJM-002-T19: Implement `ChatMessage` with default timestamp using `datetime.now()`
- [x] JJM-002-T20: Implement `SourceFile` dataclass with type hints
- [x] JJM-002-T21: Implement `JulesTask` dataclass with all fields
- [x] JJM-002-T22: Implement `JulesTask.to_dict()` method
- [x] JJM-002-T23: Implement `JulesTask.from_dict()` class method
- [x] JJM-002-T24: Handle nested object serialization in to_dict/from_dict
- [x] JJM-002-T25: Run tests (should pass - Green phase): `pytest tests/test_models.py -v`
- [x] JJM-002-T26: Add docstrings to all classes and methods
- [x] JJM-002-T27: Add type hints validation
- [x] JJM-002-T28: Run tests again to verify refactoring
- [x] JJM-002-T29: Check code coverage: `pytest tests/test_models.py --cov=src.models`
- [x] JJM-002-T30: Commit changes: "JJM-002: Implement data models with tests"
- [x] JJM-002-T31: Push to repository

---

#### JJM-003: MCP Client Foundation
**TDD: Write tests for MCP client initialization and lifecycle**

- [x] JJM-003-T01: Create `jules_job_manager/tests/test_mcp_client.py`
- [x] JJM-003-T02: Write test for `MCPClient.__init__()` with config
- [x] JJM-003-T03: Write test for `MCPClient.start()` method
- [x] JJM-003-T04: Write test for subprocess creation in start()
- [x] JJM-003-T05: Write test for stdin/stdout pipe setup
- [x] JJM-003-T06: Write test for `MCPClient.stop()` method
- [x] JJM-003-T07: Write test for process termination in stop()
- [x] JJM-003-T08: Write test for context manager `__enter__()` method
- [x] JJM-003-T09: Write test for context manager `__exit__()` method
- [x] JJM-003-T10: Write test for automatic cleanup on exit
- [x] JJM-003-T11: Write test for connection error handling
- [x] JJM-003-T12: Write test for timeout handling
- [x] JJM-003-T13: Run tests (should fail - Red phase): `pytest tests/test_mcp_client.py -v`
- [x] JJM-003-T14: Create `jules_job_manager/src/mcp_client.py`
- [x] JJM-003-T15: Implement `MCPClient` class with __init__
- [x] JJM-003-T16: Implement config loading in __init__
- [x] JJM-003-T17: Implement `start()` method with subprocess.Popen
- [x] JJM-003-T18: Set up stdin=PIPE, stdout=PIPE in Popen
- [x] JJM-003-T19: Implement `stop()` method with process.terminate()
- [x] JJM-003-T20: Add process.wait() with timeout in stop()
- [x] JJM-003-T21: Implement `__enter__()` method calling start()
- [x] JJM-003-T22: Implement `__exit__()` method calling stop()
- [x] JJM-003-T23: Add error handling for subprocess failures
- [x] JJM-003-T24: Add timeout handling for process operations
- [x] JJM-003-T25: Run tests (should pass - Green phase): `pytest tests/test_mcp_client.py -v`
- [x] JJM-003-T26: Add logging for start/stop operations
- [x] JJM-003-T27: Add docstrings to all methods
- [x] JJM-003-T28: Run tests again to verify refactoring
- [ ] JJM-003-T29: Check code coverage: `pytest tests/test_mcp_client.py --cov=src.mcp_client`
- [ ] JJM-003-T30: Commit changes: "JJM-003: Implement MCP client foundation with tests"
- [ ] JJM-003-T31: Push to repository

---

#### JJM-004: MCP Tool Invocation
**TDD: Write tests for JSON-RPC communication**

- [ ] JJM-004-T01: Add test for `_generate_request_id()` method in test_mcp_client.py
- [ ] JJM-004-T02: Write test for JSON-RPC request format
- [ ] JJM-004-T03: Write test for `_send_request()` method
- [ ] JJM-004-T04: Write test for request serialization to JSON
- [ ] JJM-004-T05: Write test for writing to stdin
- [ ] JJM-004-T06: Write test for `_read_response()` method
- [ ] JJM-004-T07: Write test for reading from stdout
- [ ] JJM-004-T08: Write test for response deserialization from JSON
- [ ] JJM-004-T09: Write test for `invoke_tool()` method
- [ ] JJM-004-T10: Write test for tool invocation with arguments
- [ ] JJM-004-T11: Write test for response parsing (success case)
- [ ] JJM-004-T12: Write test for response parsing (error case)
- [ ] JJM-004-T13: Write test for request/response correlation by ID
- [ ] JJM-004-T14: Write test for timeout in read_response
- [ ] JJM-004-T15: Write test for malformed JSON handling
- [ ] JJM-004-T16: Run tests (should fail - Red phase): `pytest tests/test_mcp_client.py::test_invoke -v`
- [ ] JJM-004-T17: Implement `_generate_request_id()` using uuid or counter
- [ ] JJM-004-T18: Implement `_send_request()` method
- [ ] JJM-004-T19: Create JSON-RPC 2.0 request structure
- [ ] JJM-004-T20: Serialize request to JSON and write to stdin
- [ ] JJM-004-T21: Add newline delimiter after JSON
- [ ] JJM-004-T22: Implement `_read_response()` method
- [ ] JJM-004-T23: Read line from stdout
- [ ] JJM-004-T24: Deserialize JSON response
- [ ] JJM-004-T25: Implement `invoke_tool()` method
- [ ] JJM-004-T26: Call _send_request with tool name and arguments
- [ ] JJM-004-T27: Call _read_response to get result
- [ ] JJM-004-T28: Parse response and extract result or error
- [ ] JJM-004-T29: Add timeout handling with select or threading
- [ ] JJM-004-T30: Add error handling for JSON parsing
- [ ] JJM-004-T31: Run tests (should pass - Green phase): `pytest tests/test_mcp_client.py -v`
- [ ] JJM-004-T32: Add request/response logging
- [ ] JJM-004-T33: Add docstrings to all methods
- [ ] JJM-004-T34: Run tests again to verify refactoring
- [ ] JJM-004-T35: Check code coverage: `pytest tests/test_mcp_client.py --cov=src.mcp_client`
- [ ] JJM-004-T36: Commit changes: "JJM-004: Implement MCP tool invocation with tests"
- [ ] JJM-004-T37: Push to repository

---

#### JJM-005: Storage Layer Implementation
**TDD: Write tests for storage operations**

- [ ] JJM-005-T01: Create `jules_job_manager/tests/test_storage.py`
- [ ] JJM-005-T02: Write test for `Storage.__init__()` with file path
- [ ] JJM-005-T03: Write test for `save_task()` method
- [ ] JJM-005-T04: Write test for saving task to JSON file
- [ ] JJM-005-T05: Write test for `get_task()` method
- [ ] JJM-005-T06: Write test for retrieving task by ID
- [ ] JJM-005-T07: Write test for `list_tasks()` method
- [ ] JJM-005-T08: Write test for listing all tasks
- [ ] JJM-005-T09: Write test for filtering tasks by status
- [ ] JJM-005-T10: Write test for `delete_task()` method
- [ ] JJM-005-T11: Write test for task not found error
- [ ] JJM-005-T12: Write test for file creation if not exists
- [ ] JJM-005-T13: Write test for concurrent access handling
- [ ] JJM-005-T14: Write test for data persistence across instances
- [ ] JJM-005-T15: Run tests (should fail - Red phase): `pytest tests/test_storage.py -v`
- [ ] JJM-005-T16: Create `jules_job_manager/src/storage.py`
- [ ] JJM-005-T17: Implement `Storage` class with __init__
- [ ] JJM-005-T18: Implement file path configuration
- [ ] JJM-005-T19: Implement `_load_data()` method to read JSON
- [ ] JJM-005-T20: Implement `_save_data()` method to write JSON
- [ ] JJM-005-T21: Implement `save_task()` method
- [ ] JJM-005-T22: Convert JulesTask to dict and save
- [ ] JJM-005-T23: Implement `get_task()` method
- [ ] JJM-005-T24: Load data and find task by ID
- [ ] JJM-005-T25: Implement `list_tasks()` method
- [ ] JJM-005-T26: Add status filtering logic
- [ ] JJM-005-T27: Implement `delete_task()` method
- [ ] JJM-005-T28: Add file locking for concurrent access
- [ ] JJM-005-T29: Add error handling for file I/O
- [ ] JJM-005-T30: Create data directory if not exists
- [ ] JJM-005-T31: Run tests (should pass - Green phase): `pytest tests/test_storage.py -v`
- [ ] JJM-005-T32: Add docstrings to all methods
- [ ] JJM-005-T33: Optimize file I/O operations
- [ ] JJM-005-T34: Run tests again to verify refactoring
- [ ] JJM-005-T35: Check code coverage: `pytest tests/test_storage.py --cov=src.storage`
- [ ] JJM-005-T36: Commit changes: "JJM-005: Implement storage layer with tests"
- [ ] JJM-005-T37: Push to repository

---

### Phase 2: Core Features (Days 3-4)

#### JJM-006: Job Manager Core Structure
**TDD: Write tests for JobManager initialization**

- [ ] JJM-006-T01: Create `jules_job_manager/tests/test_job_manager.py`
- [ ] JJM-006-T02: Write test for `JobManager.__init__()` with dependencies
- [ ] JJM-006-T03: Write test for MCPClient injection
- [ ] JJM-006-T04: Write test for Storage injection
- [ ] JJM-006-T05: Write test for dependency validation
- [ ] JJM-006-T06: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py -v`
- [ ] JJM-006-T07: Create `jules_job_manager/src/job_manager.py`
- [ ] JJM-006-T08: Implement `JobManager` class
- [ ] JJM-006-T09: Implement __init__ with mcp_client parameter
- [ ] JJM-006-T10: Implement __init__ with storage parameter
- [ ] JJM-006-T11: Add dependency validation in __init__
- [ ] JJM-006-T12: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py -v`
- [ ] JJM-006-T13: Add docstrings to class and __init__
- [ ] JJM-006-T14: Run tests again to verify refactoring
- [ ] JJM-006-T15: Commit changes: "JJM-006: Implement JobManager core structure with tests"
- [ ] JJM-006-T16: Push to repository

---

#### JJM-007: Job Manager - List Tasks
**TDD: Write tests for list_tasks functionality**

- [ ] JJM-007-T01: Write test for `list_tasks()` method in test_job_manager.py
- [ ] JJM-007-T02: Write test for listing all tasks
- [ ] JJM-007-T03: Write test for filtering by status="pending"
- [ ] JJM-007-T04: Write test for filtering by status="in_progress"
- [ ] JJM-007-T05: Write test for filtering by status="completed"
- [ ] JJM-007-T06: Write test for empty task list
- [ ] JJM-007-T07: Write test for storage integration
- [ ] JJM-007-T08: Write test for return type (List[JulesTask])
- [ ] JJM-007-T09: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_list -v`
- [ ] JJM-007-T10: Implement `list_tasks()` method in JobManager
- [ ] JJM-007-T11: Add status parameter with default None
- [ ] JJM-007-T12: Call storage.list_tasks(status)
- [ ] JJM-007-T13: Return list of JulesTask objects
- [ ] JJM-007-T14: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_list -v`
- [ ] JJM-007-T15: Add docstring to list_tasks method
- [ ] JJM-007-T16: Add type hints
- [ ] JJM-007-T17: Run tests again to verify refactoring
- [ ] JJM-007-T18: Check code coverage for list_tasks
- [ ] JJM-007-T19: Commit changes: "JJM-007: Implement list_tasks with tests"
- [ ] JJM-007-T20: Push to repository

---

#### JJM-008: Job Manager - Get Task Details
**TDD: Write tests for get_task functionality**

- [ ] JJM-008-T01: Write test for `get_task()` method in test_job_manager.py
- [ ] JJM-008-T02: Write test for getting task by valid ID
- [ ] JJM-008-T03: Write test for MCP tool invocation (jules_get_task)
- [ ] JJM-008-T04: Write test for response parsing
- [ ] JJM-008-T05: Write test for JulesTask object creation
- [ ] JJM-008-T06: Write test for storage update after fetch
- [ ] JJM-008-T07: Write test for task not found error
- [ ] JJM-008-T08: Write test for invalid task ID format
- [ ] JJM-008-T09: Write test for MCP communication error
- [ ] JJM-008-T10: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_get -v`
- [ ] JJM-008-T11: Implement `get_task()` method in JobManager
- [ ] JJM-008-T12: Add task_id parameter
- [ ] JJM-008-T13: Call mcp_client.invoke_tool("jules_get_task", {"taskId": task_id})
- [ ] JJM-008-T14: Parse response text to extract task details
- [ ] JJM-008-T15: Create JulesTask object from parsed data
- [ ] JJM-008-T16: Call storage.save_task() to update local storage
- [ ] JJM-008-T17: Return JulesTask object
- [ ] JJM-008-T18: Add error handling for task not found
- [ ] JJM-008-T19: Add error handling for invalid ID format
- [ ] JJM-008-T20: Add error handling for MCP errors
- [ ] JJM-008-T21: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_get -v`
- [ ] JJM-008-T22: Add docstring to get_task method
- [ ] JJM-008-T23: Add type hints
- [ ] JJM-008-T24: Add logging for operations
- [ ] JJM-008-T25: Run tests again to verify refactoring
- [ ] JJM-008-T26: Check code coverage for get_task
- [ ] JJM-008-T27: Commit changes: "JJM-008: Implement get_task with tests"
- [ ] JJM-008-T28: Push to repository

---

#### JJM-009: Job Manager - Create Task
**TDD: Write tests for create_task functionality**

- [ ] JJM-009-T01: Write test for `create_task()` method in test_job_manager.py
- [ ] JJM-009-T02: Write test for creating task with description and repository
- [ ] JJM-009-T03: Write test for optional branch parameter
- [ ] JJM-009-T04: Write test for MCP tool invocation (jules_create_task)
- [ ] JJM-009-T05: Write test for response parsing to extract task ID
- [ ] JJM-009-T06: Write test for JulesTask object creation
- [ ] JJM-009-T07: Write test for storage save after creation
- [ ] JJM-009-T08: Write test for repository format validation
- [ ] JJM-009-T09: Write test for invalid repository format error
- [ ] JJM-009-T10: Write test for task creation failure
- [ ] JJM-009-T11: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_create -v`
- [ ] JJM-009-T12: Implement `create_task()` method in JobManager
- [ ] JJM-009-T13: Add parameters: description, repository, branch="main"
- [ ] JJM-009-T14: Validate repository format with regex
- [ ] JJM-009-T15: Call mcp_client.invoke_tool("jules_create_task", args)
- [ ] JJM-009-T16: Parse response to extract task ID and URL
- [ ] JJM-009-T17: Create JulesTask object with initial status "pending"
- [ ] JJM-009-T18: Call storage.save_task() to persist
- [ ] JJM-009-T19: Return JulesTask object
- [ ] JJM-009-T20: Add error handling for invalid repository format
- [ ] JJM-009-T21: Add error handling for creation failures
- [ ] JJM-009-T22: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_create -v`
- [ ] JJM-009-T23: Add docstring to create_task method
- [ ] JJM-009-T24: Add type hints
- [ ] JJM-009-T25: Add logging for task creation
- [ ] JJM-009-T26: Run tests again to verify refactoring
- [ ] JJM-009-T27: Check code coverage for create_task
- [ ] JJM-009-T28: Commit changes: "JJM-009: Implement create_task with tests"
- [ ] JJM-009-T29: Push to repository

---

### Phase 3: Advanced Operations (Days 5-6)

#### JJM-010: Job Manager - Send Message
**TDD: Write tests for send_message functionality**

- [ ] JJM-010-T01: Write test for `send_message()` method in test_job_manager.py
- [ ] JJM-010-T02: Write test for sending message with task_id and message
- [ ] JJM-010-T03: Write test for MCP tool invocation (jules_send_message)
- [ ] JJM-010-T04: Write test for success response (returns True)
- [ ] JJM-010-T05: Write test for failure response (returns False)
- [ ] JJM-010-T06: Write test for storage update with new chat message
- [ ] JJM-010-T07: Write test for invalid task ID error
- [ ] JJM-010-T08: Write test for message send failure
- [ ] JJM-010-T09: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_send_message -v`
- [ ] JJM-010-T10: Implement `send_message()` method in JobManager
- [ ] JJM-010-T11: Add parameters: task_id, message
- [ ] JJM-010-T12: Call mcp_client.invoke_tool("jules_send_message", args)
- [ ] JJM-010-T13: Parse response for success/failure
- [ ] JJM-010-T14: If successful, get task from storage
- [ ] JJM-010-T15: Add new ChatMessage to task.chat_history
- [ ] JJM-010-T16: Save updated task to storage
- [ ] JJM-010-T17: Return boolean success status
- [ ] JJM-010-T18: Add error handling for invalid task ID
- [ ] JJM-010-T19: Add error handling for send failures
- [ ] JJM-010-T20: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_send_message -v`
- [ ] JJM-010-T21: Add docstring to send_message method
- [ ] JJM-010-T22: Add type hints
- [ ] JJM-010-T23: Add logging for message operations
- [ ] JJM-010-T24: Run tests again to verify refactoring
- [ ] JJM-010-T25: Check code coverage for send_message
- [ ] JJM-010-T26: Commit changes: "JJM-010: Implement send_message with tests"
- [ ] JJM-010-T27: Push to repository

---

#### JJM-011: Job Manager - Approve Plan
**TDD: Write tests for approve_plan functionality**

- [ ] JJM-011-T01: Write test for `approve_plan()` method in test_job_manager.py
- [ ] JJM-011-T02: Write test for approving plan with task_id
- [ ] JJM-011-T03: Write test for MCP tool invocation (jules_approve_plan)
- [ ] JJM-011-T04: Write test for success response (returns True)
- [ ] JJM-011-T05: Write test for failure response (returns False)
- [ ] JJM-011-T06: Write test for task status update to "in_progress"
- [ ] JJM-011-T07: Write test for task not in approval state error
- [ ] JJM-011-T08: Write test for approval failure
- [ ] JJM-011-T09: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_approve -v`
- [ ] JJM-011-T10: Implement `approve_plan()` method in JobManager
- [ ] JJM-011-T11: Add parameter: task_id
- [ ] JJM-011-T12: Call mcp_client.invoke_tool("jules_approve_plan", {"taskId": task_id})
- [ ] JJM-011-T13: Parse response for success/failure
- [ ] JJM-011-T14: If successful, get task from storage
- [ ] JJM-011-T15: Update task.status to "in_progress"
- [ ] JJM-011-T16: Save updated task to storage
- [ ] JJM-011-T17: Return boolean success status
- [ ] JJM-011-T18: Add error handling for invalid state
- [ ] JJM-011-T19: Add error handling for approval failures
- [ ] JJM-011-T20: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_approve -v`
- [ ] JJM-011-T21: Add docstring to approve_plan method
- [ ] JJM-011-T22: Add type hints
- [ ] JJM-011-T23: Add logging for approval operations
- [ ] JJM-011-T24: Run tests again to verify refactoring
- [ ] JJM-011-T25: Check code coverage for approve_plan
- [ ] JJM-011-T26: Commit changes: "JJM-011: Implement approve_plan with tests"
- [ ] JJM-011-T27: Push to repository

---

#### JJM-012: Job Manager - Resume Task
**TDD: Write tests for resume_task functionality**

- [ ] JJM-012-T01: Write test for `resume_task()` method in test_job_manager.py
- [ ] JJM-012-T02: Write test for resuming task with task_id
- [ ] JJM-012-T03: Write test for MCP tool invocation (jules_resume_task)
- [ ] JJM-012-T04: Write test for success response (returns True)
- [ ] JJM-012-T05: Write test for failure response (returns False)
- [ ] JJM-012-T06: Write test for task status update from "paused" to "in_progress"
- [ ] JJM-012-T07: Write test for task not in paused state error
- [ ] JJM-012-T08: Write test for resume failure
- [ ] JJM-012-T09: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_resume -v`
- [ ] JJM-012-T10: Implement `resume_task()` method in JobManager
- [ ] JJM-012-T11: Add parameter: task_id
- [ ] JJM-012-T12: Call mcp_client.invoke_tool("jules_resume_task", {"taskId": task_id})
- [ ] JJM-012-T13: Parse response for success/failure
- [ ] JJM-012-T14: If successful, get task from storage
- [ ] JJM-012-T15: Update task.status to "in_progress"
- [ ] JJM-012-T16: Save updated task to storage
- [ ] JJM-012-T17: Return boolean success status
- [ ] JJM-012-T18: Add error handling for invalid state
- [ ] JJM-012-T19: Add error handling for resume failures
- [ ] JJM-012-T20: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_resume -v`
- [ ] JJM-012-T21: Add docstring to resume_task method
- [ ] JJM-012-T22: Add type hints
- [ ] JJM-012-T23: Add logging for resume operations
- [ ] JJM-012-T24: Run tests again to verify refactoring
- [ ] JJM-012-T25: Check code coverage for resume_task
- [ ] JJM-012-T26: Commit changes: "JJM-012: Implement resume_task with tests"
- [ ] JJM-012-T27: Push to repository

---

#### JJM-013: Job Manager - Monitor Task
**TDD: Write tests for monitor_task functionality**

- [ ] JJM-013-T01: Write test for `monitor_task()` method in test_job_manager.py
- [ ] JJM-013-T02: Write test for monitoring with task_id and interval
- [ ] JJM-013-T03: Write test for polling loop with time.sleep
- [ ] JJM-013-T04: Write test for calling get_task in loop
- [ ] JJM-013-T05: Write test for status change detection
- [ ] JJM-013-T06: Write test for exit on "completed" status
- [ ] JJM-013-T07: Write test for KeyboardInterrupt handling
- [ ] JJM-013-T08: Write test for progress display
- [ ] JJM-013-T09: Write test for task not found error
- [ ] JJM-013-T10: Run tests (should fail - Red phase): `pytest tests/test_job_manager.py::test_monitor -v`
- [ ] JJM-013-T11: Implement `monitor_task()` method in JobManager
- [ ] JJM-013-T12: Add parameters: task_id, interval=30
- [ ] JJM-013-T13: Create while loop for polling
- [ ] JJM-013-T14: Call get_task(task_id) in loop
- [ ] JJM-013-T15: Display current status with timestamp
- [ ] JJM-013-T16: Check if status == "completed" and break
- [ ] JJM-013-T17: Call time.sleep(interval)
- [ ] JJM-013-T18: Wrap loop in try-except for KeyboardInterrupt
- [ ] JJM-013-T19: Display "Monitoring stopped" on interrupt
- [ ] JJM-013-T20: Add error handling for task not found
- [ ] JJM-013-T21: Run tests (should pass - Green phase): `pytest tests/test_job_manager.py::test_monitor -v`
- [ ] JJM-013-T22: Add rich library for progress display
- [ ] JJM-013-T23: Add docstring to monitor_task method
- [ ] JJM-013-T24: Add type hints
- [ ] JJM-013-T25: Add logging for monitoring operations
- [ ] JJM-013-T26: Run tests again to verify refactoring
- [ ] JJM-013-T27: Check code coverage for monitor_task
- [ ] JJM-013-T28: Commit changes: "JJM-013: Implement monitor_task with tests"
- [ ] JJM-013-T29: Push to repository

---

### Phase 4: CLI Interface (Day 7)

#### JJM-014: CLI - Main Entry Point and Argument Parser
**TDD: Write tests for CLI main function**

- [ ] JJM-014-T01: Create `jules_job_manager/tests/test_main.py`
- [ ] JJM-014-T02: Write test for `main()` function existence
- [ ] JJM-014-T03: Write test for ArgumentParser creation
- [ ] JJM-014-T04: Write test for subparsers creation
- [ ] JJM-014-T05: Write test for "list" subcommand registration
- [ ] JJM-014-T06: Write test for "get" subcommand registration
- [ ] JJM-014-T07: Write test for "create" subcommand registration
- [ ] JJM-014-T08: Write test for "message" subcommand registration
- [ ] JJM-014-T09: Write test for "approve" subcommand registration
- [ ] JJM-014-T10: Write test for "resume" subcommand registration
- [ ] JJM-014-T11: Write test for "monitor" subcommand registration
- [ ] JJM-014-T12: Write test for --version flag
- [ ] JJM-014-T13: Write test for --config flag
- [ ] JJM-014-T14: Write test for config loading
- [ ] JJM-014-T15: Write test for MCPClient initialization
- [ ] JJM-014-T16: Write test for JobManager initialization
- [ ] JJM-014-T17: Write test for context manager usage
- [ ] JJM-014-T18: Write test for exit code 0 on success
- [ ] JJM-014-T19: Write test for exit code 1 on error
- [ ] JJM-014-T20: Run tests (should fail - Red phase): `pytest tests/test_main.py -v`
- [ ] JJM-014-T21: Create `jules_job_manager/src/main.py`
- [ ] JJM-014-T22: Import argparse, MCPClient, JobManager, Storage
- [ ] JJM-014-T23: Implement `main()` function
- [ ] JJM-014-T24: Create ArgumentParser with description
- [ ] JJM-014-T25: Add --version argument
- [ ] JJM-014-T26: Add --config argument
- [ ] JJM-014-T27: Create subparsers
- [ ] JJM-014-T28: Add "list" subcommand with --status argument
- [ ] JJM-014-T29: Add "get" subcommand with task_id argument
- [ ] JJM-014-T30: Add "create" subcommand with --repo, --description, --branch
- [ ] JJM-014-T31: Add "message" subcommand with task_id and message
- [ ] JJM-014-T32: Add "approve" subcommand with task_id
- [ ] JJM-014-T33: Add "resume" subcommand with task_id
- [ ] JJM-014-T34: Add "monitor" subcommand with task_id and --interval
- [ ] JJM-014-T35: Implement config loading function
- [ ] JJM-014-T36: Initialize MCPClient with config
- [ ] JJM-014-T37: Initialize Storage with config
- [ ] JJM-014-T38: Initialize JobManager with dependencies
- [ ] JJM-014-T39: Use context manager for MCPClient
- [ ] JJM-014-T40: Route to appropriate handler based on subcommand
- [ ] JJM-014-T41: Add try-except for error handling
- [ ] JJM-014-T42: Return exit code 0 on success, 1 on error
- [ ] JJM-014-T43: Run tests (should pass - Green phase): `pytest tests/test_main.py -v`
- [ ] JJM-014-T44: Add docstrings to main function
- [ ] JJM-014-T45: Add type hints
- [ ] JJM-014-T46: Run tests again to verify refactoring
- [ ] JJM-014-T47: Check code coverage for main
- [ ] JJM-014-T48: Commit changes: "JJM-014: Implement CLI main entry point with tests"
- [ ] JJM-014-T49: Push to repository

---

#### JJM-015: CLI - List Command
**TDD: Write tests for list command handler**

- [ ] JJM-015-T01: Write test for `handle_list()` function in test_main.py
- [ ] JJM-015-T02: Write test for calling job_manager.list_tasks()
- [ ] JJM-015-T03: Write test for status filter parameter
- [ ] JJM-015-T04: Write test for table output with rich
- [ ] JJM-015-T05: Write test for empty list handling
- [ ] JJM-015-T06: Write test for error handling
- [ ] JJM-015-T07: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_list -v`
- [ ] JJM-015-T08: Implement `handle_list()` function in main.py
- [ ] JJM-015-T09: Add parameters: args, job_manager
- [ ] JJM-015-T10: Extract status from args.status
- [ ] JJM-015-T11: Call job_manager.list_tasks(status)
- [ ] JJM-015-T12: Create rich Table with columns
- [ ] JJM-015-T13: Add rows for each task (ID, Repository, Status, Updated)
- [ ] JJM-015-T14: Truncate task ID to 8 characters
- [ ] JJM-015-T15: Format timestamp as "YYYY-MM-DD HH:MM"
- [ ] JJM-015-T16: Color code status (green, yellow, blue, red)
- [ ] JJM-015-T17: Handle empty list with message
- [ ] JJM-015-T18: Add error handling
- [ ] JJM-015-T19: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_list -v`
- [ ] JJM-015-T20: Add docstring to handle_list
- [ ] JJM-015-T21: Run tests again to verify refactoring
- [ ] JJM-015-T22: Test manually: `python -m jules_job_manager list`
- [ ] JJM-015-T23: Commit changes: "JJM-015: Implement list command with tests"
- [ ] JJM-015-T24: Push to repository

---

#### JJM-016: CLI - Get Command
**TDD: Write tests for get command handler**

- [ ] JJM-016-T01: Write test for `handle_get()` function in test_main.py
- [ ] JJM-016-T02: Write test for calling job_manager.get_task()
- [ ] JJM-016-T03: Write test for task details display with rich Panel
- [ ] JJM-016-T04: Write test for source files display
- [ ] JJM-016-T05: Write test for chat messages display
- [ ] JJM-016-T06: Write test for task not found error
- [ ] JJM-016-T07: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_get -v`
- [ ] JJM-016-T08: Implement `handle_get()` function in main.py
- [ ] JJM-016-T09: Add parameters: args, job_manager
- [ ] JJM-016-T10: Extract task_id from args.task_id
- [ ] JJM-016-T11: Call job_manager.get_task(task_id)
- [ ] JJM-016-T12: Create rich Panel for task details
- [ ] JJM-016-T13: Display: ID, Title, Repository, Branch, Status, Created, Updated, URL
- [ ] JJM-016-T14: Display source files with emoji indicators
- [ ] JJM-016-T15: Display recent chat messages (last 5)
- [ ] JJM-016-T16: Add error handling for task not found
- [ ] JJM-016-T17: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_get -v`
- [ ] JJM-016-T18: Add docstring to handle_get
- [ ] JJM-016-T19: Run tests again to verify refactoring
- [ ] JJM-016-T20: Test manually: `python -m jules_job_manager get <task_id>`
- [ ] JJM-016-T21: Commit changes: "JJM-016: Implement get command with tests"
- [ ] JJM-016-T22: Push to repository

---

#### JJM-017: CLI - Create Command
**TDD: Write tests for create command handler**

- [ ] JJM-017-T01: Write test for `handle_create()` function in test_main.py
- [ ] JJM-017-T02: Write test for calling job_manager.create_task()
- [ ] JJM-017-T03: Write test for repository format validation
- [ ] JJM-017-T04: Write test for success message display
- [ ] JJM-017-T05: Write test for progress indicator
- [ ] JJM-017-T06: Write test for invalid repository format error
- [ ] JJM-017-T07: Write test for creation failure error
- [ ] JJM-017-T08: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_create -v`
- [ ] JJM-017-T09: Implement `handle_create()` function in main.py
- [ ] JJM-017-T10: Add parameters: args, job_manager
- [ ] JJM-017-T11: Extract repo, description, branch from args
- [ ] JJM-017-T12: Validate repository format with regex
- [ ] JJM-017-T13: Show progress indicator with rich.Progress
- [ ] JJM-017-T14: Call job_manager.create_task(description, repo, branch)
- [ ] JJM-017-T15: Display success message with task ID and URL
- [ ] JJM-017-T16: Add error handling for invalid format
- [ ] JJM-017-T17: Add error handling for creation failure
- [ ] JJM-017-T18: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_create -v`
- [ ] JJM-017-T19: Add docstring to handle_create
- [ ] JJM-017-T20: Run tests again to verify refactoring
- [ ] JJM-017-T21: Test manually: `python -m jules_job_manager create --repo owner/repo --description "test"`
- [ ] JJM-017-T22: Commit changes: "JJM-017: Implement create command with tests"
- [ ] JJM-017-T23: Push to repository

---

#### JJM-018: CLI - Message Command
**TDD: Write tests for message command handler**

- [ ] JJM-018-T01: Write test for `handle_message()` function in test_main.py
- [ ] JJM-018-T02: Write test for calling job_manager.send_message()
- [ ] JJM-018-T03: Write test for success confirmation display
- [ ] JJM-018-T04: Write test for task not found error
- [ ] JJM-018-T05: Write test for send failure error
- [ ] JJM-018-T06: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_message -v`
- [ ] JJM-018-T07: Implement `handle_message()` function in main.py
- [ ] JJM-018-T08: Add parameters: args, job_manager
- [ ] JJM-018-T09: Extract task_id and message from args
- [ ] JJM-018-T10: Call job_manager.send_message(task_id, message)
- [ ] JJM-018-T11: Display success confirmation
- [ ] JJM-018-T12: Suggest using 'get' command to see response
- [ ] JJM-018-T13: Add error handling for task not found
- [ ] JJM-018-T14: Add error handling for send failure
- [ ] JJM-018-T15: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_message -v`
- [ ] JJM-018-T16: Add docstring to handle_message
- [ ] JJM-018-T17: Run tests again to verify refactoring
- [ ] JJM-018-T18: Test manually: `python -m jules_job_manager message <task_id> "test message"`
- [ ] JJM-018-T19: Commit changes: "JJM-018: Implement message command with tests"
- [ ] JJM-018-T20: Push to repository

---

#### JJM-019: CLI - Approve Command
**TDD: Write tests for approve command handler**

- [ ] JJM-019-T01: Write test for `handle_approve()` function in test_main.py
- [ ] JJM-019-T02: Write test for calling job_manager.approve_plan()
- [ ] JJM-019-T03: Write test for success confirmation display
- [ ] JJM-019-T04: Write test for task not found error
- [ ] JJM-019-T05: Write test for approval failure error
- [ ] JJM-019-T06: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_approve -v`
- [ ] JJM-019-T07: Implement `handle_approve()` function in main.py
- [ ] JJM-019-T08: Add parameters: args, job_manager
- [ ] JJM-019-T09: Extract task_id from args
- [ ] JJM-019-T10: Call job_manager.approve_plan(task_id)
- [ ] JJM-019-T11: Display success confirmation
- [ ] JJM-019-T12: Suggest using 'monitor' command to track progress
- [ ] JJM-019-T13: Add error handling for task not found
- [ ] JJM-019-T14: Add error handling for approval failure
- [ ] JJM-019-T15: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_approve -v`
- [ ] JJM-019-T16: Add docstring to handle_approve
- [ ] JJM-019-T17: Run tests again to verify refactoring
- [ ] JJM-019-T18: Test manually: `python -m jules_job_manager approve <task_id>`
- [ ] JJM-019-T19: Commit changes: "JJM-019: Implement approve command with tests"
- [ ] JJM-019-T20: Push to repository

---

#### JJM-020: CLI - Resume Command
**TDD: Write tests for resume command handler**

- [ ] JJM-020-T01: Write test for `handle_resume()` function in test_main.py
- [ ] JJM-020-T02: Write test for calling job_manager.resume_task()
- [ ] JJM-020-T03: Write test for success confirmation display
- [ ] JJM-020-T04: Write test for task not found error
- [ ] JJM-020-T05: Write test for resume failure error
- [ ] JJM-020-T06: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_resume -v`
- [ ] JJM-020-T07: Implement `handle_resume()` function in main.py
- [ ] JJM-020-T08: Add parameters: args, job_manager
- [ ] JJM-020-T09: Extract task_id from args
- [ ] JJM-020-T10: Call job_manager.resume_task(task_id)
- [ ] JJM-020-T11: Display success confirmation
- [ ] JJM-020-T12: Suggest using 'monitor' command to track progress
- [ ] JJM-020-T13: Add error handling for task not found
- [ ] JJM-020-T14: Add error handling for resume failure
- [ ] JJM-020-T15: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_resume -v`
- [ ] JJM-020-T16: Add docstring to handle_resume
- [ ] JJM-020-T17: Run tests again to verify refactoring
- [ ] JJM-020-T18: Test manually: `python -m jules_job_manager resume <task_id>`
- [ ] JJM-020-T19: Commit changes: "JJM-020: Implement resume command with tests"
- [ ] JJM-020-T20: Push to repository

---

#### JJM-021: CLI - Monitor Command
**TDD: Write tests for monitor command handler**

- [ ] JJM-021-T01: Write test for `handle_monitor()` function in test_main.py
- [ ] JJM-021-T02: Write test for calling job_manager.monitor_task()
- [ ] JJM-021-T03: Write test for interval parameter
- [ ] JJM-021-T04: Write test for live status updates
- [ ] JJM-021-T05: Write test for KeyboardInterrupt handling
- [ ] JJM-021-T06: Write test for task not found error
- [ ] JJM-021-T07: Run tests (should fail - Red phase): `pytest tests/test_main.py::test_handle_monitor -v`
- [ ] JJM-021-T08: Implement `handle_monitor()` function in main.py
- [ ] JJM-021-T09: Add parameters: args, job_manager
- [ ] JJM-021-T10: Extract task_id and interval from args
- [ ] JJM-021-T11: Call job_manager.monitor_task(task_id, interval)
- [ ] JJM-021-T12: Display "Monitoring stopped" on exit
- [ ] JJM-021-T13: Add error handling for task not found
- [ ] JJM-021-T14: Run tests (should pass - Green phase): `pytest tests/test_main.py::test_handle_monitor -v`
- [ ] JJM-021-T15: Add docstring to handle_monitor
- [ ] JJM-021-T16: Run tests again to verify refactoring
- [ ] JJM-021-T17: Test manually: `python -m jules_job_manager monitor <task_id>`
- [ ] JJM-021-T18: Commit changes: "JJM-021: Implement monitor command with tests"
- [ ] JJM-021-T19: Push to repository

---

### Phase 5: Testing & Documentation (Day 8)

#### JJM-022: Unit Tests - MCP Client
**TDD: Comprehensive test coverage for MCP Client**

- [ ] JJM-022-T01: Review existing tests in test_mcp_client.py
- [ ] JJM-022-T02: Write test for server startup timeout
- [ ] JJM-022-T03: Write test for server crash during operation
- [ ] JJM-022-T04: Write test for malformed JSON response
- [ ] JJM-022-T05: Write test for missing response fields
- [ ] JJM-022-T06: Write test for request ID mismatch
- [ ] JJM-022-T07: Write test for concurrent requests
- [ ] JJM-022-T08: Write test for large response handling
- [ ] JJM-022-T09: Write test for connection cleanup on error
- [ ] JJM-022-T10: Run all MCP client tests: `pytest tests/test_mcp_client.py -v`
- [ ] JJM-022-T11: Check code coverage: `pytest tests/test_mcp_client.py --cov=src.mcp_client --cov-report=html`
- [ ] JJM-022-T12: Review coverage report and identify gaps
- [ ] JJM-022-T13: Write additional tests for uncovered code paths
- [ ] JJM-022-T14: Run tests again and verify >80% coverage
- [ ] JJM-022-T15: Commit changes: "JJM-022: Add comprehensive MCP client tests"
- [ ] JJM-022-T16: Push to repository

---

#### JJM-023: Unit Tests - Job Manager
**TDD: Comprehensive test coverage for Job Manager**

- [ ] JJM-023-T01: Review existing tests in test_job_manager.py
- [ ] JJM-023-T02: Write test for error handling in list_tasks
- [ ] JJM-023-T03: Write test for error handling in get_task
- [ ] JJM-023-T04: Write test for error handling in create_task
- [ ] JJM-023-T05: Write test for error handling in send_message
- [ ] JJM-023-T06: Write test for error handling in approve_plan
- [ ] JJM-023-T07: Write test for error handling in resume_task
- [ ] JJM-023-T08: Write test for error handling in monitor_task
- [ ] JJM-023-T09: Write test for data transformation edge cases
- [ ] JJM-023-T10: Write test for storage integration failures
- [ ] JJM-023-T11: Run all job manager tests: `pytest tests/test_job_manager.py -v`
- [ ] JJM-023-T12: Check code coverage: `pytest tests/test_job_manager.py --cov=src.job_manager --cov-report=html`
- [ ] JJM-023-T13: Review coverage report and identify gaps
- [ ] JJM-023-T14: Write additional tests for uncovered code paths
- [ ] JJM-023-T15: Run tests again and verify >80% coverage
- [ ] JJM-023-T16: Commit changes: "JJM-023: Add comprehensive job manager tests"
- [ ] JJM-023-T17: Push to repository

---

#### JJM-024: Integration Tests
**TDD: End-to-end workflow tests**

- [ ] JJM-024-T01: Create `jules_job_manager/tests/test_integration.py`
- [ ] JJM-024-T02: Write test for complete task creation workflow
- [ ] JJM-024-T03: Write test for task monitoring workflow
- [ ] JJM-024-T04: Write test for message sending workflow
- [ ] JJM-024-T05: Write test for approval workflow
- [ ] JJM-024-T06: Write test for resume workflow
- [ ] JJM-024-T07: Write test for error recovery scenarios
- [ ] JJM-024-T08: Write test for data persistence across operations
- [ ] JJM-024-T09: Set up test fixtures for integration tests
- [ ] JJM-024-T10: Set up test cleanup after each test
- [ ] JJM-024-T11: Run integration tests: `pytest tests/test_integration.py -v -m integration`
- [ ] JJM-024-T12: Fix any failing integration tests
- [ ] JJM-024-T13: Add pytest markers for integration tests
- [ ] JJM-024-T14: Document how to run integration tests
- [ ] JJM-024-T15: Commit changes: "JJM-024: Add integration tests"
- [ ] JJM-024-T16: Push to repository

---

#### JJM-025: Documentation - README and Usage Guide
**Documentation: Create comprehensive user documentation**

- [ ] JJM-025-T01: Create `jules_job_manager/README.md`
- [ ] JJM-025-T02: Write project description section
- [ ] JJM-025-T03: Write features section
- [ ] JJM-025-T04: Write installation instructions (pip install)
- [ ] JJM-025-T05: Write installation instructions (from source)
- [ ] JJM-025-T06: Write dependencies section
- [ ] JJM-025-T07: Write configuration guide (config.json)
- [ ] JJM-025-T08: Write configuration guide (environment variables)
- [ ] JJM-025-T09: Write usage examples for list command
- [ ] JJM-025-T10: Write usage examples for get command
- [ ] JJM-025-T11: Write usage examples for create command
- [ ] JJM-025-T12: Write usage examples for message command
- [ ] JJM-025-T13: Write usage examples for approve command
- [ ] JJM-025-T14: Write usage examples for resume command
- [ ] JJM-025-T15: Write usage examples for monitor command
- [ ] JJM-025-T16: Write troubleshooting section
- [ ] JJM-025-T17: Write common errors and solutions
- [ ] JJM-025-T18: Write contributing guidelines
- [ ] JJM-025-T19: Write license information
- [ ] JJM-025-T20: Add code examples from plan Appendix B
- [ ] JJM-025-T21: Add screenshots or ASCII art for CLI output
- [ ] JJM-025-T22: Link to main project README for MCP server setup
- [ ] JJM-025-T23: Review and proofread documentation
- [ ] JJM-025-T24: Run all tests to verify MVP completion: `pytest tests/ -v`
- [ ] JJM-025-T25: Commit changes: "JJM-025: Add comprehensive documentation"
- [ ] JJM-025-T26: Push to repository
- [ ] JJM-025-T27: Tag MVP release: `git tag v0.1.0-mvp`
- [ ] JJM-025-T28: Push tag: `git push origin v0.1.0-mvp`

---

**MVP COMPLETION CHECKPOINT**
- [ ] All MVP tests passing: `pytest tests/ -v`
- [ ] Code coverage >80%: `pytest tests/ --cov=src --cov-report=html`
- [ ] Documentation complete and reviewed
- [ ] MVP tagged and released

---


