# Jules Job Manager - Development Tickets

This document contains all development tickets for implementing the Python Jules Job Manager, organized by development phase.

---

## Part 1: MVP Development Tickets (8 Days)

### Phase 1: Foundation (Days 1-2)

#### JJM-001: Project Structure Setup
**Title:** Initialize Python project structure and configuration

**Description:**
Set up the complete project directory structure for the Jules Job Manager, including all necessary directories, configuration files, and initial Python package setup.

**Acceptance Criteria:**
- [ ] Directory structure created as per plan (src/, tests/, config/, data/)
- [ ] `__init__.py` files created in all Python packages
- [ ] `requirements.txt` created with initial dependencies
- [ ] `setup.py` created with project metadata
- [ ] `.env.example` created with all required environment variables
- [ ] Project can be installed in development mode (`pip install -e .`)

**Dependencies:** None

**Estimated Effort:** 2 hours

**Phase:** MVP Phase 1: Foundation

**Files to Create:**
- `jules_job_manager/src/__init__.py`
- `jules_job_manager/src/main.py` (empty placeholder)
- `jules_job_manager/src/mcp_client.py` (empty placeholder)
- `jules_job_manager/src/job_manager.py` (empty placeholder)
- `jules_job_manager/src/models.py` (empty placeholder)
- `jules_job_manager/src/storage.py` (empty placeholder)
- `jules_job_manager/tests/__init__.py`
- `jules_job_manager/tests/test_mcp_client.py` (empty placeholder)
- `jules_job_manager/tests/test_job_manager.py` (empty placeholder)
- `jules_job_manager/config/config.json`
- `jules_job_manager/requirements.txt`
- `jules_job_manager/setup.py`
- `jules_job_manager/.env.example`
- `jules_job_manager/README.md`

**Technical Notes:**
- Use Python 3.9+ as minimum version
- Initial dependencies: `rich`, `python-dotenv`
- Setup.py should use setuptools
- Config.json should match structure in plan section 1.8

**Blocks:** JJM-002, JJM-003, JJM-004, JJM-005

---

#### JJM-002: Data Models Implementation
**Title:** Implement core data models for tasks, messages, and files

**Description:**
Create Python dataclasses for all data models as specified in the plan: TaskStatus enum, SourceFile, ChatMessage, and JulesTask. Include proper type hints, validation, and serialization methods.

**Acceptance Criteria:**
- [ ] `TaskStatus` enum created with all status values (pending, in_progress, completed, paused, waiting_approval)
- [ ] `SourceFile` dataclass created with filename, url, status fields
- [ ] `ChatMessage` dataclass created with timestamp, content, type fields
- [ ] `JulesTask` dataclass created with all fields from plan section 1.5
- [ ] All dataclasses have `to_dict()` method for JSON serialization
- [ ] All dataclasses have `from_dict()` class method for deserialization
- [ ] Type hints are complete and correct
- [ ] Docstrings added to all classes and methods

**Dependencies:** JJM-001

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 1: Foundation

**Files to Create/Modify:**
- `jules_job_manager/src/models.py`

**Technical Notes:**
- Use `from dataclasses import dataclass`
- Use `from enum import Enum` for TaskStatus
- Use `from typing import List, Optional`
- Use `from datetime import datetime`
- Implement ISO format for datetime serialization
- Example structure from plan section 1.5

**Blocks:** JJM-004, JJM-005, JJM-006

---

#### JJM-003: MCP Client - JSON-RPC Foundation
**Title:** Implement JSON-RPC 2.0 communication layer for MCP

**Description:**
Create the MCPClient class with methods to start the Node.js MCP server process, send JSON-RPC requests via stdin, receive responses via stdout, and handle request/response correlation.

**Acceptance Criteria:**
- [ ] `MCPClient` class created with `__init__(server_path: str)` constructor
- [ ] `_start_server()` method starts Node.js process using subprocess.Popen
- [ ] `_send_request(method: str, params: dict) -> dict` method implemented
- [ ] Request ID generation and correlation implemented
- [ ] JSON-RPC 2.0 format correctly implemented (jsonrpc: "2.0", id, method, params)
- [ ] Response parsing handles both success and error responses
- [ ] `_stop_server()` method gracefully terminates the Node.js process
- [ ] Context manager support (`__enter__` and `__exit__`) for automatic cleanup
- [ ] Error handling for connection failures and timeouts

**Dependencies:** JJM-001

**Estimated Effort:** 6 hours

**Phase:** MVP Phase 1: Foundation

**Files to Create/Modify:**
- `jules_job_manager/src/mcp_client.py`

**Technical Notes:**
- Use `subprocess.Popen` with stdin=PIPE, stdout=PIPE, stderr=PIPE
- Use `json.dumps()` and `json.loads()` for serialization
- Implement request ID as incrementing integer or UUID
- Store pending requests in dict for correlation
- Use threading or select for non-blocking I/O if needed
- Reference plan section 1.6.1 for function signatures
- Node.js server path from config: `../google-jules-mcp/dist/index.js`

**Blocks:** JJM-004, JJM-007

---

#### JJM-004: MCP Client - Tool Invocation
**Title:** Implement MCP tool invocation methods

**Description:**
Add methods to MCPClient for listing available tools and calling specific tools. Implement the `call_tool()` and `list_tools()` methods that use the JSON-RPC foundation to interact with the MCP server.

**Acceptance Criteria:**
- [ ] `list_tools() -> List[dict]` method implemented
- [ ] `call_tool(tool_name: str, arguments: dict) -> dict` method implemented
- [ ] Method sends "tools/list" JSON-RPC request for list_tools()
- [ ] Method sends "tools/call" JSON-RPC request for call_tool()
- [ ] Response parsing extracts tool results correctly
- [ ] Error handling for tool not found, invalid arguments
- [ ] Return values match expected format from MCP server
- [ ] Unit tests for both methods with mocked subprocess

**Dependencies:** JJM-001, JJM-003

**Estimated Effort:** 4 hours

**Phase:** MVP Phase 1: Foundation

**Files to Create/Modify:**
- `jules_job_manager/src/mcp_client.py`
- `jules_job_manager/tests/test_mcp_client.py`

**Technical Notes:**
- JSON-RPC method for listing tools: "tools/list"
- JSON-RPC method for calling tools: "tools/call"
- Parameters for call_tool: {"name": tool_name, "arguments": arguments}
- Parse response content from MCP server format
- Reference README.md for available tools (jules_create_task, jules_get_task, etc.)

**Blocks:** JJM-006, JJM-007, JJM-008, JJM-009, JJM-010

---

#### JJM-005: Storage Layer Implementation
**Title:** Implement local JSON storage for task persistence

**Description:**
Create the Storage class that handles reading and writing task data to a local JSON file. Implement methods for saving, retrieving, listing, and deleting tasks with proper file locking and error handling.

**Acceptance Criteria:**
- [ ] `Storage` class created with `__init__(data_path: str)` constructor
- [ ] `save_task(task: JulesTask) -> None` method implemented
- [ ] `get_task(task_id: str) -> Optional[JulesTask]` method implemented
- [ ] `list_tasks() -> List[JulesTask]` method implemented
- [ ] `delete_task(task_id: str) -> bool` method implemented
- [ ] JSON file created automatically if it doesn't exist
- [ ] Directory created automatically if it doesn't exist
- [ ] File locking implemented to prevent concurrent write issues
- [ ] Proper error handling for file I/O errors
- [ ] Data validation when loading from file

**Dependencies:** JJM-001, JJM-002

**Estimated Effort:** 4 hours

**Phase:** MVP Phase 1: Foundation

**Files to Create/Modify:**
- `jules_job_manager/src/storage.py`

**Technical Notes:**
- Use `pathlib.Path` for path handling
- Use `json.dump()` and `json.load()` for serialization
- Default data path: `./data/tasks.json`
- File format: `{"tasks": [...]}`
- Use `fcntl.flock()` on Unix or `msvcrt.locking()` on Windows for file locking
- Convert JulesTask objects to/from dict using model methods
- Reference plan section 1.6.3 for function signatures

**Blocks:** JJM-006, JJM-011

---

### Phase 2: Core Features (Days 3-4)

#### JJM-006: Job Manager - Core Class Structure
**Title:** Implement JobManager core class and initialization

**Description:**
Create the JobManager class that orchestrates interactions between the MCP client and storage layer. Implement the constructor and basic helper methods.

**Acceptance Criteria:**
- [ ] `JobManager` class created with `__init__(mcp_client: MCPClient, storage: Storage)` constructor
- [ ] Instance variables for mcp_client and storage properly initialized
- [ ] `_parse_task_response(response: dict) -> JulesTask` helper method implemented
- [ ] `_format_task_output(task: JulesTask) -> str` helper method implemented
- [ ] Error handling wrapper methods for common operations
- [ ] Logging setup for job manager operations
- [ ] Configuration loading from config.json

**Dependencies:** JJM-002, JJM-004, JJM-005

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 2: Core Features

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`

**Technical Notes:**
- Reference plan section 1.6.2 for class structure
- Use logging module for operation logging
- Parse MCP response format: `{"content": [{"type": "text", "text": "..."}]}`
- Extract task data from text responses

**Blocks:** JJM-007, JJM-008, JJM-009, JJM-010, JJM-011, JJM-012

---

#### JJM-007: Job Manager - List Tasks
**Title:** Implement list_tasks functionality

**Description:**
Implement the `list_tasks()` method in JobManager that retrieves tasks from both the MCP server and local storage, with optional status filtering.

**Acceptance Criteria:**
- [ ] `list_tasks(status_filter: Optional[str] = None) -> List[JulesTask]` method implemented
- [ ] Method calls MCP tool "jules_list_tasks" with appropriate parameters
- [ ] Results merged with local storage data
- [ ] Status filtering works correctly (pending, in_progress, completed, paused, all)
- [ ] Tasks sorted by updated_at timestamp (most recent first)
- [ ] Local cache updated with fresh data from MCP server
- [ ] Error handling for MCP server failures (fallback to local cache)
- [ ] Unit tests with mocked MCP client

**Dependencies:** JJM-004, JJM-006

**Estimated Effort:** 4 hours

**Phase:** MVP Phase 2: Core Features

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- MCP tool name: "jules_list_tasks"
- MCP arguments: {"status": status_filter, "limit": 100}
- Parse response text to extract task list
- Merge strategy: prefer MCP data, fallback to local if task not in MCP response
- Update local storage with merged results

**Blocks:** JJM-013

---

#### JJM-008: Job Manager - Get Task Details
**Title:** Implement get_task functionality

**Description:**
Implement the `get_task()` method in JobManager that retrieves detailed information about a specific task from the MCP server and updates local storage.

**Acceptance Criteria:**
- [ ] `get_task(task_id: str) -> JulesTask` method implemented
- [ ] Method calls MCP tool "jules_get_task" with task ID
- [ ] Response parsed to create JulesTask object
- [ ] Local storage updated with fresh task data
- [ ] Chat history and source files properly extracted
- [ ] Error handling for task not found
- [ ] Error handling for invalid task ID format
- [ ] Unit tests with mocked MCP client

**Dependencies:** JJM-004, JJM-006

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 2: Core Features

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- MCP tool name: "jules_get_task"
- MCP arguments: {"taskId": task_id}
- Parse response text to extract task details, status, source files, chat messages
- Handle both task ID and full URL formats
- Update storage after successful retrieval

**Blocks:** JJM-013, JJM-014

---

#### JJM-009: Job Manager - Create Task
**Title:** Implement create_task functionality

**Description:**
Implement the `create_task()` method in JobManager that creates a new Jules task via the MCP server and stores it locally.

**Acceptance Criteria:**
- [ ] `create_task(description: str, repository: str, branch: str = "main") -> JulesTask` method implemented
- [ ] Method calls MCP tool "jules_create_task" with appropriate parameters
- [ ] Response parsed to extract new task ID and URL
- [ ] JulesTask object created with initial status "pending"
- [ ] Task saved to local storage
- [ ] Validation for repository format (owner/repo)
- [ ] Error handling for task creation failures
- [ ] Unit tests with mocked MCP client

**Dependencies:** JJM-004, JJM-006

**Estimated Effort:** 4 hours

**Phase:** MVP Phase 2: Core Features

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- MCP tool name: "jules_create_task"
- MCP arguments: {"description": description, "repository": repository, "branch": branch}
- Parse response to extract task ID from URL or text
- Repository format validation: must match "owner/repo-name" pattern
- Initial task status should be "pending"

**Blocks:** JJM-013

---

### Phase 3: Advanced Operations (Days 5-6)

#### JJM-010: Job Manager - Send Message
**Title:** Implement send_message functionality

**Description:**
Implement the `send_message()` method in JobManager that sends messages or instructions to an active Jules task.

**Acceptance Criteria:**
- [ ] `send_message(task_id: str, message: str) -> bool` method implemented
- [ ] Method calls MCP tool "jules_send_message" with task ID and message
- [ ] Success/failure status returned
- [ ] Local task updated with new chat message
- [ ] Error handling for invalid task ID
- [ ] Error handling for message send failures
- [ ] Unit tests with mocked MCP client

**Dependencies:** JJM-004, JJM-006

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 3: Advanced Operations

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- MCP tool name: "jules_send_message"
- MCP arguments: {"taskId": task_id, "message": message}
- Add message to local task's chat_history after successful send
- Message type should be "user"

**Blocks:** JJM-013

---

#### JJM-011: Job Manager - Approve Plan
**Title:** Implement approve_plan functionality

**Description:**
Implement the `approve_plan()` method in JobManager that approves a Jules execution plan for a task.

**Acceptance Criteria:**
- [ ] `approve_plan(task_id: str) -> bool` method implemented
- [ ] Method calls MCP tool "jules_approve_plan" with task ID
- [ ] Success/failure status returned
- [ ] Local task status updated if approval successful
- [ ] Error handling for task not in approval state
- [ ] Error handling for approval failures
- [ ] Unit tests with mocked MCP client

**Dependencies:** JJM-004, JJM-006

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 3: Advanced Operations

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- MCP tool name: "jules_approve_plan"
- MCP arguments: {"taskId": task_id}
- Update task status to "in_progress" after approval
- Handle case where no approval is needed

**Blocks:** JJM-013

---

#### JJM-012: Job Manager - Resume Task
**Title:** Implement resume_task functionality

**Description:**
Implement the `resume_task()` method in JobManager that resumes a paused Jules task.

**Acceptance Criteria:**
- [ ] `resume_task(task_id: str) -> bool` method implemented
- [ ] Method calls MCP tool "jules_resume_task" with task ID
- [ ] Success/failure status returned
- [ ] Local task status updated to "in_progress" if successful
- [ ] Error handling for task not in paused state
- [ ] Error handling for resume failures
- [ ] Unit tests with mocked MCP client

**Dependencies:** JJM-004, JJM-006

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 3: Advanced Operations

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- MCP tool name: "jules_resume_task"
- MCP arguments: {"taskId": task_id}
- Update task status from "paused" to "in_progress"
- Handle case where task is not paused

**Blocks:** JJM-013

---

#### JJM-013: Job Manager - Monitor Task
**Title:** Implement monitor_task functionality with polling

**Description:**
Implement the `monitor_task()` method in JobManager that continuously polls a task's status and displays updates until completion or user interruption.

**Acceptance Criteria:**
- [ ] `monitor_task(task_id: str, interval: int = 30) -> None` method implemented
- [ ] Method polls task status at specified interval (default 30 seconds)
- [ ] Status changes displayed to user with timestamps
- [ ] Monitoring continues until task reaches "completed" status
- [ ] User can interrupt monitoring with Ctrl+C (graceful handling)
- [ ] Progress indicator shown during polling
- [ ] Error handling for task not found
- [ ] Unit tests with mocked time.sleep and MCP client

**Dependencies:** JJM-006, JJM-007, JJM-008

**Estimated Effort:** 5 hours

**Phase:** MVP Phase 3: Advanced Operations

**Files to Create/Modify:**
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- Use `time.sleep(interval)` for polling delay
- Call `get_task()` method in loop to fetch latest status
- Use `rich` library for progress display and status formatting
- Handle KeyboardInterrupt for graceful exit
- Display: timestamp, status, source files count, latest chat message
- Exit conditions: status == "completed" or KeyboardInterrupt

**Blocks:** JJM-014

---

### Phase 4: CLI Interface (Day 7)

#### JJM-014: CLI - Main Entry Point and Argument Parser
**Title:** Implement CLI main entry point with argparse

**Description:**
Create the main CLI entry point with argparse-based command structure. Implement the main() function and subcommand parsers for all operations.

**Acceptance Criteria:**
- [ ] `main()` function created in main.py
- [ ] ArgumentParser configured with all subcommands (list, get, create, message, approve, resume, monitor)
- [ ] Each subcommand has appropriate arguments and help text
- [ ] Configuration loading from config.json and environment variables
- [ ] MCPClient and JobManager initialization in main()
- [ ] Error handling and user-friendly error messages
- [ ] Exit codes: 0 for success, 1 for errors
- [ ] `--version` flag shows version information
- [ ] `--config` flag allows custom config file path

**Dependencies:** JJM-006, JJM-007, JJM-008, JJM-009, JJM-010, JJM-011, JJM-012, JJM-013

**Estimated Effort:** 6 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Use `argparse.ArgumentParser` with subparsers
- Command structure from plan section 1.7
- Load config from: 1) config.json, 2) environment variables, 3) CLI args (priority order)
- Use context manager for MCPClient to ensure cleanup
- Implement each subcommand as separate function (handle_list, handle_get, etc.)
- Use `rich.console.Console` for formatted output

**Blocks:** JJM-015, JJM-016, JJM-017, JJM-018, JJM-019, JJM-020, JJM-021

---

#### JJM-015: CLI - List Command
**Title:** Implement 'list' CLI command

**Description:**
Implement the CLI handler for the 'list' command that displays all tasks with optional status filtering.

**Acceptance Criteria:**
- [ ] `handle_list(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager list [--status STATUS]`
- [ ] Status filter options: all, pending, in_progress, completed, paused
- [ ] Output formatted as table using rich library
- [ ] Table columns: ID (truncated), Repository, Status, Updated
- [ ] Empty list handled gracefully with message
- [ ] Error handling with user-friendly messages

**Dependencies:** JJM-014

**Estimated Effort:** 2 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Use `rich.table.Table` for formatted output
- Truncate task ID to first 8 characters for display
- Format timestamp as "YYYY-MM-DD HH:MM"
- Color code status: green=completed, yellow=in_progress, blue=pending, red=paused

---

#### JJM-016: CLI - Get Command
**Title:** Implement 'get' CLI command

**Description:**
Implement the CLI handler for the 'get' command that displays detailed information about a specific task.

**Acceptance Criteria:**
- [ ] `handle_get(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager get TASK_ID`
- [ ] Output shows: ID, Title, Repository, Branch, Status, Created, Updated, URL
- [ ] Source files listed with status indicators
- [ ] Recent chat messages displayed (last 5)
- [ ] Output formatted using rich panels and syntax highlighting
- [ ] Error handling for task not found

**Dependencies:** JJM-014

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Use `rich.panel.Panel` for task details
- Use `rich.syntax.Syntax` for code/diff display if available
- Display full task ID, not truncated
- Show source files with emoji indicators: ✏️ modified, ➕ created, ❌ deleted

---

#### JJM-017: CLI - Create Command
**Title:** Implement 'create' CLI command

**Description:**
Implement the CLI handler for the 'create' command that creates a new Jules task.

**Acceptance Criteria:**
- [ ] `handle_create(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager create --repo REPO --description DESC [--branch BRANCH]`
- [ ] Repository format validated (owner/repo)
- [ ] Default branch is "main" if not specified
- [ ] Success message shows task ID and URL
- [ ] Progress indicator shown during task creation
- [ ] Error handling for invalid repository format
- [ ] Error handling for task creation failures

**Dependencies:** JJM-014

**Estimated Effort:** 2 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Use `rich.progress.Progress` for creation indicator
- Validate repository format with regex: `^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$`
- Display success message with task URL for easy access

---

#### JJM-018: CLI - Message Command
**Title:** Implement 'message' CLI command

**Description:**
Implement the CLI handler for the 'message' command that sends a message to a Jules task.

**Acceptance Criteria:**
- [ ] `handle_message(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager message TASK_ID "MESSAGE"`
- [ ] Message sent to specified task
- [ ] Success confirmation displayed
- [ ] Error handling for task not found
- [ ] Error handling for message send failures

**Dependencies:** JJM-014

**Estimated Effort:** 2 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Quote handling for multi-word messages
- Display confirmation: "Message sent to task {task_id}"
- Suggest using 'get' command to see response

---

#### JJM-019: CLI - Approve Command
**Title:** Implement 'approve' CLI command

**Description:**
Implement the CLI handler for the 'approve' command that approves a Jules execution plan.

**Acceptance Criteria:**
- [ ] `handle_approve(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager approve TASK_ID`
- [ ] Plan approval sent to specified task
- [ ] Success confirmation displayed
- [ ] Error handling for task not found
- [ ] Error handling for task not in approval state

**Dependencies:** JJM-014

**Estimated Effort:** 2 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Display confirmation: "Plan approved for task {task_id}"
- Suggest using 'monitor' command to track progress

---

#### JJM-020: CLI - Resume Command
**Title:** Implement 'resume' CLI command

**Description:**
Implement the CLI handler for the 'resume' command that resumes a paused Jules task.

**Acceptance Criteria:**
- [ ] `handle_resume(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager resume TASK_ID`
- [ ] Task resume sent to specified task
- [ ] Success confirmation displayed
- [ ] Error handling for task not found
- [ ] Error handling for task not in paused state

**Dependencies:** JJM-014

**Estimated Effort:** 2 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Display confirmation: "Task {task_id} resumed"
- Suggest using 'monitor' command to track progress

---

#### JJM-021: CLI - Monitor Command
**Title:** Implement 'monitor' CLI command

**Description:**
Implement the CLI handler for the 'monitor' command that continuously monitors a task's status.

**Acceptance Criteria:**
- [ ] `handle_monitor(args, job_manager)` function implemented
- [ ] Command: `python -m jules_job_manager monitor TASK_ID [--interval SECONDS]`
- [ ] Default interval is 30 seconds
- [ ] Live status updates displayed
- [ ] User can interrupt with Ctrl+C
- [ ] Final status shown on exit
- [ ] Error handling for task not found

**Dependencies:** JJM-014

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 4: CLI Interface

**Files to Create/Modify:**
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Use `rich.live.Live` for updating display
- Show: current status, elapsed time, last update time, source files count
- Handle KeyboardInterrupt gracefully
- Display "Monitoring stopped" message on exit

---

### Phase 5: Testing & Documentation (Day 8)

#### JJM-022: Unit Tests - MCP Client
**Title:** Write comprehensive unit tests for MCP Client

**Description:**
Create unit tests for all MCPClient methods with mocked subprocess and JSON-RPC communication.

**Acceptance Criteria:**
- [ ] Test server startup and shutdown
- [ ] Test JSON-RPC request formatting
- [ ] Test response parsing (success and error cases)
- [ ] Test request/response correlation
- [ ] Test connection error handling
- [ ] Test timeout handling
- [ ] Test context manager functionality
- [ ] Code coverage > 80% for mcp_client.py

**Dependencies:** JJM-003, JJM-004

**Estimated Effort:** 4 hours

**Phase:** MVP Phase 5: Testing & Documentation

**Files to Create/Modify:**
- `jules_job_manager/tests/test_mcp_client.py`

**Technical Notes:**
- Use `unittest.mock` for subprocess mocking
- Mock stdin/stdout communication
- Test both successful and error responses
- Use pytest fixtures for common setup

---

#### JJM-023: Unit Tests - Job Manager
**Title:** Write comprehensive unit tests for Job Manager

**Description:**
Create unit tests for all JobManager methods with mocked MCP client and storage.

**Acceptance Criteria:**
- [ ] Test all job manager methods (list, get, create, message, approve, resume, monitor)
- [ ] Test error handling for each method
- [ ] Test data parsing and transformation
- [ ] Test storage integration
- [ ] Test status filtering
- [ ] Code coverage > 80% for job_manager.py

**Dependencies:** JJM-006, JJM-007, JJM-008, JJM-009, JJM-010, JJM-011, JJM-012, JJM-013

**Estimated Effort:** 6 hours

**Phase:** MVP Phase 5: Testing & Documentation

**Files to Create/Modify:**
- `jules_job_manager/tests/test_job_manager.py`

**Technical Notes:**
- Mock MCPClient and Storage classes
- Use pytest parametrize for testing multiple scenarios
- Test edge cases (empty lists, invalid IDs, etc.)

---

#### JJM-024: Integration Tests
**Title:** Write integration tests for end-to-end workflows

**Description:**
Create integration tests that test complete workflows from CLI to MCP server interaction.

**Acceptance Criteria:**
- [ ] Test complete task creation workflow
- [ ] Test task monitoring workflow
- [ ] Test message sending workflow
- [ ] Test approval workflow
- [ ] Tests can run against mock MCP server or real server (configurable)
- [ ] Tests clean up created resources

**Dependencies:** JJM-014, JJM-015, JJM-016, JJM-017, JJM-018, JJM-019, JJM-020, JJM-021

**Estimated Effort:** 4 hours

**Phase:** MVP Phase 5: Testing & Documentation

**Files to Create/Modify:**
- `jules_job_manager/tests/test_integration.py`

**Technical Notes:**
- Use pytest fixtures for test setup/teardown
- Consider using docker-compose for test environment
- Mark tests with `@pytest.mark.integration` for selective running

---

#### JJM-025: Documentation - README and Usage Guide
**Title:** Write comprehensive README and usage documentation

**Description:**
Create detailed README with installation instructions, usage examples, and troubleshooting guide.

**Acceptance Criteria:**
- [ ] README.md includes project description
- [ ] Installation instructions (pip install, dependencies)
- [ ] Configuration guide (config.json, environment variables)
- [ ] Usage examples for all CLI commands
- [ ] Troubleshooting section
- [ ] Contributing guidelines
- [ ] License information

**Dependencies:** JJM-014, JJM-015, JJM-016, JJM-017, JJM-018, JJM-019, JJM-020, JJM-021

**Estimated Effort:** 3 hours

**Phase:** MVP Phase 5: Testing & Documentation

**Files to Create/Modify:**
- `jules_job_manager/README.md`

**Technical Notes:**
- Include code examples from plan Appendix B
- Add screenshots or ASCII art for CLI output
- Link to main project README for MCP server setup

---

## Part 2: Production Enhancement Tickets (8 Weeks)

> **Note:** Production enhancement tickets are also available in separate files:
> - `docs/tickets_production.md` - Phases 1-3 (Weeks 1-3)
> - `docs/tickets_production_part2.md` - Phase 4 (Week 4)
> - `docs/tickets_production_part3.md` - Phases 5-8 (Weeks 5-8)

For the complete list of 37 production tickets (JJM-026 to JJM-062), please refer to the separate production ticket files listed above. These tickets cover:

### Phase 1: Error Handling & Logging (Week 1)
- JJM-026: Custom Exception Hierarchy
- JJM-027: Retry Logic with Tenacity
- JJM-028: Structured Logging with Structlog
- JJM-029: Enhanced Error Handling in All Components

### Phase 2: Database Integration (Week 2)
- JJM-030: Database Schema Design and Migration Setup
- JJM-031: Database Storage Implementation
- JJM-032: Task Event Logging
- JJM-033: Configuration for Storage Backend Selection

### Phase 3: Caching & Performance (Week 3)
- JJM-034: Redis Integration Setup
- JJM-035: Task Caching Implementation
- JJM-036: Real-time Updates with Redis Pub/Sub
- JJM-037: Performance Optimization

### Phase 4: Web API (Week 4)
- JJM-038: FastAPI Application Setup
- JJM-039: API - Task Management Endpoints
- JJM-040: API - Task Operations Endpoints
- JJM-041: API - Monitoring Endpoints
- JJM-042: API Authentication
- JJM-043: API Testing

### Phase 5: Testing (Week 5)
- JJM-044: Async Operations Support
- JJM-045: Integration Test Suite
- JJM-046: Performance Testing
- JJM-047: End-to-End Testing

### Phase 6: Monitoring & Metrics (Week 6)
- JJM-048: Prometheus Metrics Implementation
- JJM-049: Health Check System
- JJM-050: Alerting Configuration
- JJM-051: Grafana Dashboard

### Phase 7: Security & Compliance (Week 7)
- JJM-052: Secrets Management
- JJM-053: Input Validation and Sanitization
- JJM-054: Audit Logging
- JJM-055: Rate Limiting
- JJM-056: Security Audit and Penetration Testing

### Phase 8: Deployment & Documentation (Week 8)
- JJM-057: Docker Image Creation
- JJM-058: Docker Compose for Production
- JJM-059: CI/CD Pipeline
- JJM-060: User Documentation
- JJM-061: Developer Documentation
- JJM-062: Production Deployment

---

## Complete Ticket Summary

### MVP Tickets: 25 tickets (JJM-001 to JJM-025)
- **Phase 1 (Foundation):** 5 tickets, ~20 hours
- **Phase 2 (Core Features):** 4 tickets, ~14 hours
- **Phase 3 (Advanced Operations):** 5 tickets, ~17 hours
- **Phase 4 (CLI Interface):** 8 tickets, ~20 hours
- **Phase 5 (Testing & Documentation):** 3 tickets, ~11 hours
- **Total MVP Effort:** ~82 hours (~10 days with 8-hour days)

### Production Tickets: 37 tickets (JJM-026 to JJM-062)
- **Phase 1 (Error Handling & Logging):** 4 tickets, ~22 hours
- **Phase 2 (Database Integration):** 4 tickets, ~21 hours
- **Phase 3 (Caching & Performance):** 4 tickets, ~21 hours
- **Phase 4 (Web API):** 6 tickets, ~37 hours
- **Phase 5 (Testing):** 4 tickets, ~38 hours
- **Phase 6 (Monitoring & Metrics):** 4 tickets, ~22 hours
- **Phase 7 (Security & Compliance):** 5 tickets, ~30 hours
- **Phase 8 (Deployment & Documentation):** 6 tickets, ~37 hours
- **Total Production Effort:** ~228 hours (~29 days with 8-hour days)

### Grand Total: 62 tickets, ~310 hours (~39 days)

---

## Quick Reference

### Independent Tickets (Can Start Immediately):
- JJM-001 (Project Structure)
- JJM-026 (Custom Exceptions)
- JJM-030 (Database Schema)
- JJM-034 (Redis Setup)
- JJM-038 (FastAPI Setup)
- JJM-052 (Secrets Management)
- JJM-057 (Docker Image)

### Critical Path:
JJM-001 → JJM-002 → JJM-005 → JJM-006 → JJM-007 → JJM-013 → JJM-014 → JJM-015 → JJM-022 → JJM-024 → JJM-025

### Parallel Work Opportunities:
- Database (JJM-030 to JJM-033) || Caching (JJM-034 to JJM-037)
- API (JJM-038 to JJM-043) || Async (JJM-044)
- Docs (JJM-060, JJM-061) || Deployment (JJM-057 to JJM-059)
- Security (JJM-052 to JJM-056) || Monitoring (JJM-048 to JJM-051)

---


