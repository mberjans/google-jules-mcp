# Jules Job Manager - Production Enhancement Tickets

This document contains all production enhancement tickets for the Jules Job Manager (Weeks 1-8).

---

## Part 2: Production Enhancement Tickets (8 Weeks)

### Phase 1: Error Handling & Logging (Week 1)

#### JJM-026: Custom Exception Hierarchy
**Title:** Implement custom exception hierarchy for error handling

**Description:**
Create a comprehensive exception hierarchy for all error types in the Jules Job Manager, including base exceptions and specific error types.

**Acceptance Criteria:**
- [ ] `JulesManagerError` base exception class created
- [ ] `MCPConnectionError` exception for MCP server connection failures
- [ ] `AuthenticationError` exception for Jules authentication failures
- [ ] `TaskNotFoundError` exception for task not found errors
- [ ] `OperationFailedError` exception for operation failures
- [ ] `ConfigurationError` exception for configuration issues
- [ ] All exceptions include helpful error messages and context
- [ ] Exception hierarchy documented in docstrings

**Dependencies:** None (can start immediately)

**Estimated Effort:** 3 hours

**Phase:** Production Phase 1: Error Handling & Logging

**Files to Create/Modify:**
- `jules_job_manager/src/exceptions.py`

**Technical Notes:**
- Reference plan section 2.4.1
- Each exception should accept message and optional context dict
- Include `__str__` and `__repr__` methods for debugging
- Add error codes for programmatic error handling

**Blocks:** JJM-027, JJM-028

---

#### JJM-027: Retry Logic with Tenacity
**Title:** Implement retry logic for transient failures

**Description:**
Add retry logic using the tenacity library for operations that may fail transiently (network issues, temporary server unavailability).

**Acceptance Criteria:**
- [ ] Tenacity library added to requirements.txt
- [ ] Retry decorators created for MCP client methods
- [ ] Exponential backoff configured (start: 1s, max: 60s)
- [ ] Maximum retry attempts configurable (default: 3)
- [ ] Retry only on specific exceptions (connection errors, timeouts)
- [ ] Logging of retry attempts
- [ ] Circuit breaker pattern for persistent failures

**Dependencies:** JJM-026

**Estimated Effort:** 5 hours

**Phase:** Production Phase 1: Error Handling & Logging

**Files to Create/Modify:**
- `jules_job_manager/src/mcp_client.py`
- `jules_job_manager/src/retry_config.py`
- `jules_job_manager/requirements.txt`

**Technical Notes:**
- Use `tenacity.retry` decorator
- Configure with `wait_exponential` and `stop_after_attempt`
- Use `retry_if_exception_type` for selective retries
- Implement circuit breaker with failure threshold (5 failures = open circuit)
- Reference plan section 2.4.1

**Blocks:** JJM-029

---

#### JJM-028: Structured Logging with Structlog
**Title:** Implement structured logging throughout the application

**Description:**
Replace basic logging with structured logging using structlog for better log analysis and debugging.

**Acceptance Criteria:**
- [ ] Structlog library added to requirements.txt
- [ ] Logging configuration module created
- [ ] All log statements converted to structured format
- [ ] Log levels properly used (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- [ ] Context added to log entries (task_id, operation, user, etc.)
- [ ] JSON output format for production
- [ ] Human-readable format for development
- [ ] Log rotation configured (daily, 30-day retention)

**Dependencies:** JJM-026

**Estimated Effort:** 6 hours

**Phase:** Production Phase 1: Error Handling & Logging

**Files to Create/Modify:**
- `jules_job_manager/src/logging_config.py`
- `jules_job_manager/src/mcp_client.py`
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/src/main.py`
- `jules_job_manager/requirements.txt`

**Technical Notes:**
- Reference plan section 2.4.2
- Use `structlog.get_logger()` for logger instances
- Configure processors: add_log_level, add_timestamp, JSONRenderer
- Use `logging.handlers.TimedRotatingFileHandler` for rotation
- Log file path: configurable, default `logs/jules_manager.log`

**Blocks:** JJM-029

---

#### JJM-029: Enhanced Error Handling in All Components
**Title:** Add comprehensive error handling to all components

**Description:**
Update all components (MCP client, job manager, storage, CLI) with comprehensive error handling using custom exceptions and retry logic.

**Acceptance Criteria:**
- [ ] All MCP client methods wrapped with retry logic
- [ ] All job manager methods have try-except blocks with custom exceptions
- [ ] Storage operations handle file I/O errors gracefully
- [ ] CLI displays user-friendly error messages
- [ ] All errors logged with appropriate context
- [ ] Error recovery strategies implemented where possible
- [ ] Unit tests for error scenarios

**Dependencies:** JJM-026, JJM-027, JJM-028

**Estimated Effort:** 8 hours

**Phase:** Production Phase 1: Error Handling & Logging

**Files to Create/Modify:**
- `jules_job_manager/src/mcp_client.py`
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/src/storage.py`
- `jules_job_manager/src/main.py`
- `jules_job_manager/tests/test_error_handling.py`

**Technical Notes:**
- Wrap all external calls (subprocess, file I/O, network) with error handling
- Use custom exceptions for domain-specific errors
- Implement fallback strategies (e.g., use cache if MCP server unavailable)
- Log full stack traces for debugging

---

### Phase 2: Database Integration (Week 2)

#### JJM-030: Database Schema Design and Migration Setup
**Title:** Design PostgreSQL schema and set up Alembic migrations

**Description:**
Create the database schema for tasks, chat messages, source files, and task events. Set up Alembic for database migrations.

**Acceptance Criteria:**
- [ ] SQLAlchemy and Alembic added to requirements.txt
- [ ] Database models created for: Task, ChatMessage, SourceFile, TaskEvent
- [ ] Alembic initialized with migration directory
- [ ] Initial migration created with all tables
- [ ] Indexes created for common queries (task status, repository, timestamp)
- [ ] Foreign key constraints properly defined
- [ ] Migration can be applied and rolled back successfully

**Dependencies:** None (can start immediately)

**Estimated Effort:** 6 hours

**Phase:** Production Phase 2: Database Integration

**Files to Create/Modify:**
- `jules_job_manager/src/db_models.py`
- `jules_job_manager/alembic.ini`
- `jules_job_manager/alembic/env.py`
- `jules_job_manager/alembic/versions/001_initial_schema.py`
- `jules_job_manager/requirements.txt`

**Technical Notes:**
- Reference plan section 2.4.4 for schema design
- Use SQLAlchemy declarative base
- JSONB column for metadata in tasks table
- Timestamps with timezone support
- Use UUID or VARCHAR(255) for task IDs

**Blocks:** JJM-031, JJM-032

---

#### JJM-031: Database Storage Implementation
**Title:** Implement PostgreSQL storage backend

**Description:**
Create a new storage implementation that uses PostgreSQL instead of JSON files, implementing the same interface as the JSON storage.

**Acceptance Criteria:**
- [ ] `DatabaseStorage` class created implementing Storage interface
- [ ] Connection pooling configured
- [ ] All CRUD operations implemented (save, get, list, delete)
- [ ] Transactions used for data consistency
- [ ] Query optimization with proper indexes
- [ ] Connection string from configuration
- [ ] Graceful handling of connection failures
- [ ] Unit tests with test database

**Dependencies:** JJM-030

**Estimated Effort:** 8 hours

**Phase:** Production Phase 2: Database Integration

**Files to Create/Modify:**
- `jules_job_manager/src/db_storage.py`
- `jules_job_manager/src/storage.py` (add factory method)
- `jules_job_manager/tests/test_db_storage.py`

**Technical Notes:**
- Use SQLAlchemy session management
- Implement connection pooling with `create_engine(pool_size=10)`
- Use context managers for session handling
- Convert between ORM models and dataclass models
- Reference plan section 2.4.4

**Blocks:** JJM-033, JJM-044

---

#### JJM-032: Task Event Logging
**Title:** Implement task event logging to database

**Description:**
Add event logging for all task operations (created, updated, message sent, approved, etc.) to the task_events table.

**Acceptance Criteria:**
- [ ] Event logging methods added to DatabaseStorage
- [ ] Events logged for: task_created, task_updated, message_sent, plan_approved, task_resumed
- [ ] Event data stored as JSONB with relevant context
- [ ] Event retrieval methods implemented
- [ ] Event history can be queried by task ID
- [ ] Events include timestamp and event type

**Dependencies:** JJM-030

**Estimated Effort:** 4 hours

**Phase:** Production Phase 2: Database Integration

**Files to Create/Modify:**
- `jules_job_manager/src/db_storage.py`
- `jules_job_manager/src/job_manager.py`

**Technical Notes:**
- Create `log_event(task_id, event_type, event_data)` method
- Event types as enum or constants
- Include user context if available
- Use for audit trail and debugging

**Blocks:** JJM-033

---

#### JJM-033: Configuration for Storage Backend Selection
**Title:** Add configuration to select storage backend (JSON vs PostgreSQL)

**Description:**
Update configuration system to allow selection between JSON file storage and PostgreSQL storage, with automatic initialization based on config.

**Acceptance Criteria:**
- [ ] Configuration option `storage.backend` added (values: "json", "postgresql")
- [ ] Storage factory method selects appropriate backend
- [ ] PostgreSQL connection string configurable
- [ ] Graceful fallback to JSON if PostgreSQL unavailable
- [ ] Migration guide for moving from JSON to PostgreSQL
- [ ] Environment variable support for connection string

**Dependencies:** JJM-031, JJM-032

**Estimated Effort:** 3 hours

**Phase:** Production Phase 2: Database Integration

**Files to Create/Modify:**
- `jules_job_manager/src/storage.py`
- `jules_job_manager/src/main.py`
- `jules_job_manager/config/config.yaml`
- `jules_job_manager/docs/migration_guide.md`

**Technical Notes:**
- Reference plan section 2.4.3 for config structure
- Use factory pattern for storage creation
- Connection string format: `postgresql://user:pass@host:port/dbname`
- Support DATABASE_URL environment variable

---

### Phase 3: Caching & Performance (Week 3)

#### JJM-034: Redis Integration Setup
**Title:** Set up Redis client and connection management

**Description:**
Add Redis client library and implement connection management for caching and pub/sub functionality.

**Acceptance Criteria:**
- [ ] Redis library (redis-py) added to requirements.txt
- [ ] Redis client wrapper class created
- [ ] Connection pooling configured
- [ ] Health check method implemented
- [ ] Graceful degradation if Redis unavailable
- [ ] Configuration for Redis URL and connection parameters

**Dependencies:** None (can start immediately)

**Estimated Effort:** 4 hours

**Phase:** Production Phase 3: Caching & Performance

**Files to Create/Modify:**
- `jules_job_manager/src/redis_client.py`
- `jules_job_manager/requirements.txt`
- `jules_job_manager/config/config.yaml`

**Technical Notes:**
- Use `redis.ConnectionPool` for connection pooling
- Default Redis URL: `redis://localhost:6379/0`
- Implement retry logic for connection failures
- Support Redis Sentinel for high availability

**Blocks:** JJM-035, JJM-036, JJM-045, JJM-055

---

#### JJM-035: Task Caching Implementation
**Title:** Implement Redis caching for task data

**Description:**
Add caching layer for task data to reduce database queries and improve performance.

**Acceptance Criteria:**
- [ ] Cache wrapper for storage operations
- [ ] Task details cached with 5-minute TTL
- [ ] Task lists cached with 1-minute TTL
- [ ] Cache invalidation on task updates
- [ ] Cache-aside pattern implemented
- [ ] Cache hit/miss metrics tracked
- [ ] Graceful fallback to database if cache unavailable

**Dependencies:** JJM-034

**Estimated Effort:** 6 hours

**Phase:** Production Phase 3: Caching & Performance

**Files to Create/Modify:**
- `jules_job_manager/src/cached_storage.py`
- `jules_job_manager/src/storage.py`

**Technical Notes:**
- Reference plan section 2.4.5
- Use Redis keys: `task:{task_id}`, `tasks:list:{status}`
- Serialize with JSON or pickle
- Implement cache warming for frequently accessed tasks
- Use Redis SETEX for automatic expiration

**Blocks:** JJM-037

---

#### JJM-036: Real-time Updates with Redis Pub/Sub
**Title:** Implement real-time task updates using Redis pub/sub

**Description:**
Add pub/sub functionality for real-time task status updates, allowing multiple clients to receive updates without polling.

**Acceptance Criteria:**
- [ ] Publisher publishes task updates to Redis channels
- [ ] Subscriber can listen for task updates
- [ ] Channel naming: `task:updates:{task_id}`
- [ ] Updates published on: status change, message sent, plan approved
- [ ] Monitor command can use pub/sub instead of polling (optional mode)
- [ ] Graceful fallback to polling if pub/sub unavailable

**Dependencies:** JJM-034

**Estimated Effort:** 5 hours

**Phase:** Production Phase 3: Caching & Performance

**Files to Create/Modify:**
- `jules_job_manager/src/redis_client.py`
- `jules_job_manager/src/job_manager.py`

**Technical Notes:**
- Use Redis PUBLISH for sending updates
- Use Redis SUBSCRIBE for receiving updates
- Message format: JSON with task_id, event_type, data
- Implement in separate thread for non-blocking operation

---

#### JJM-037: Performance Optimization
**Title:** Optimize database queries and add connection pooling

**Description:**
Optimize database queries, add proper indexing, and configure connection pooling for better performance.

**Acceptance Criteria:**
- [ ] Slow query analysis performed
- [ ] Indexes added for common query patterns
- [ ] N+1 query problems resolved with eager loading
- [ ] Connection pool size optimized (default: 10)
- [ ] Query result pagination implemented for large lists
- [ ] Database query logging for performance monitoring
- [ ] Performance benchmarks documented

**Dependencies:** JJM-035

**Estimated Effort:** 6 hours

**Phase:** Production Phase 3: Caching & Performance

**Files to Create/Modify:**
- `jules_job_manager/src/db_storage.py`
- `jules_job_manager/alembic/versions/002_add_indexes.py`
- `jules_job_manager/docs/performance.md`

**Technical Notes:**
- Use SQLAlchemy `joinedload` for eager loading
- Add composite indexes for common filters
- Implement cursor-based pagination
- Use EXPLAIN ANALYZE for query optimization
- Target: <100ms for common queries

---


