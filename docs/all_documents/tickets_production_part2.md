# Jules Job Manager - Production Enhancement Tickets (Part 2)

This document contains production enhancement tickets for Phases 4-8 (Weeks 4-8).

---

### Phase 4: Web API (Week 4)

#### JJM-038: FastAPI Application Setup
**Title:** Set up FastAPI application structure

**Description:**
Create FastAPI application with proper structure, middleware, CORS configuration, and health check endpoints.

**Acceptance Criteria:**
- [ ] FastAPI and uvicorn added to requirements.txt
- [ ] FastAPI app created with proper structure
- [ ] CORS middleware configured
- [ ] Request logging middleware added
- [ ] Health check endpoint implemented (`/health`)
- [ ] API versioning structure (`/api/v1/`)
- [ ] OpenAPI documentation auto-generated
- [ ] Application can start and serve requests

**Dependencies:** None (can start immediately)

**Estimated Effort:** 5 hours

**Phase:** Production Phase 4: Web API

**Files to Create/Modify:**
- `jules_job_manager/src/api/__init__.py`
- `jules_job_manager/src/api/main.py`
- `jules_job_manager/src/api/middleware.py`
- `jules_job_manager/requirements.txt`

**Technical Notes:**
- Reference plan section 2.4.6 for API structure
- Use `fastapi.middleware.cors.CORSMiddleware`
- Health check returns: status, version, uptime
- Configure uvicorn with: host, port, workers from config

**Blocks:** JJM-039, JJM-040, JJM-041, JJM-042, JJM-048

---

#### JJM-039: API - Task Management Endpoints
**Title:** Implement task management REST API endpoints

**Description:**
Create REST API endpoints for task CRUD operations (list, get, create, update, delete).

**Acceptance Criteria:**
- [ ] GET `/api/v1/tasks` - List tasks with filtering and pagination
- [ ] GET `/api/v1/tasks/{task_id}` - Get task details
- [ ] POST `/api/v1/tasks` - Create new task
- [ ] PUT `/api/v1/tasks/{task_id}` - Update task
- [ ] DELETE `/api/v1/tasks/{task_id}` - Delete task
- [ ] Request/response models defined with Pydantic
- [ ] Input validation implemented
- [ ] Error responses follow standard format
- [ ] OpenAPI documentation complete

**Dependencies:** JJM-038

**Estimated Effort:** 8 hours

**Phase:** Production Phase 4: Web API

**Files to Create/Modify:**
- `jules_job_manager/src/api/routes/tasks.py`
- `jules_job_manager/src/api/models.py`
- `jules_job_manager/src/api/main.py`

**Technical Notes:**
- Use Pydantic models for request/response validation
- Implement pagination with limit/offset or cursor
- Filter parameters: status, repository, date_range
- Return 404 for task not found, 400 for validation errors
- Use dependency injection for JobManager instance

**Blocks:** JJM-043, JJM-046

---

#### JJM-040: API - Task Operations Endpoints
**Title:** Implement task operation REST API endpoints

**Description:**
Create REST API endpoints for task operations (send message, approve plan, resume task).

**Acceptance Criteria:**
- [ ] POST `/api/v1/tasks/{task_id}/message` - Send message to task
- [ ] POST `/api/v1/tasks/{task_id}/approve` - Approve task plan
- [ ] POST `/api/v1/tasks/{task_id}/resume` - Resume paused task
- [ ] Request models defined with Pydantic
- [ ] Async operation support
- [ ] Operation status returned in response
- [ ] Error handling for invalid operations

**Dependencies:** JJM-038

**Estimated Effort:** 5 hours

**Phase:** Production Phase 4: Web API

**Files to Create/Modify:**
- `jules_job_manager/src/api/routes/operations.py`
- `jules_job_manager/src/api/models.py`
- `jules_job_manager/src/api/main.py`

**Technical Notes:**
- Use async/await for non-blocking operations
- Return operation result immediately (not async job)
- Include operation timestamp in response
- Validate task state before operations

**Blocks:** JJM-043, JJM-046

---

#### JJM-041: API - Monitoring Endpoints
**Title:** Implement monitoring and status REST API endpoints

**Description:**
Create REST API endpoints for task monitoring and event history.

**Acceptance Criteria:**
- [ ] GET `/api/v1/tasks/{task_id}/status` - Get current task status
- [ ] GET `/api/v1/tasks/{task_id}/events` - Get task event history
- [ ] WebSocket endpoint for real-time updates (optional)
- [ ] Event filtering by type and date range
- [ ] Pagination for event history

**Dependencies:** JJM-038

**Estimated Effort:** 5 hours

**Phase:** Production Phase 4: Web API

**Files to Create/Modify:**
- `jules_job_manager/src/api/routes/monitoring.py`
- `jules_job_manager/src/api/websocket.py`
- `jules_job_manager/src/api/main.py`

**Technical Notes:**
- Use FastAPI WebSocket support for real-time updates
- Event history from task_events table
- Status endpoint returns: current status, last update, progress
- WebSocket sends updates on task changes

**Blocks:** JJM-043

---

#### JJM-042: API Authentication
**Title:** Implement API key authentication

**Description:**
Add API key authentication for securing API endpoints.

**Acceptance Criteria:**
- [ ] API key authentication middleware implemented
- [ ] API keys stored securely (hashed)
- [ ] API key validation on all protected endpoints
- [ ] Health check endpoint remains public
- [ ] 401 Unauthorized response for invalid/missing keys
- [ ] API key management commands (create, revoke)
- [ ] Rate limiting per API key

**Dependencies:** JJM-038

**Estimated Effort:** 6 hours

**Phase:** Production Phase 4: Web API

**Files to Create/Modify:**
- `jules_job_manager/src/api/auth.py`
- `jules_job_manager/src/api/middleware.py`
- `jules_job_manager/src/cli/api_keys.py`

**Technical Notes:**
- Use FastAPI dependency injection for auth
- API key in header: `X-API-Key` or `Authorization: Bearer <key>`
- Store hashed keys in database
- Use secrets module for key generation
- Implement rate limiting with Redis

**Blocks:** JJM-043, JJM-055

---

#### JJM-043: API Testing
**Title:** Write comprehensive API tests

**Description:**
Create integration tests for all API endpoints using FastAPI TestClient.

**Acceptance Criteria:**
- [ ] Tests for all task management endpoints
- [ ] Tests for all operation endpoints
- [ ] Tests for authentication
- [ ] Tests for error scenarios (404, 400, 401)
- [ ] Tests for pagination and filtering
- [ ] Tests use test database
- [ ] Code coverage > 80% for API code

**Dependencies:** JJM-039, JJM-040, JJM-041, JJM-042

**Estimated Effort:** 8 hours

**Phase:** Production Phase 4: Web API

**Files to Create/Modify:**
- `jules_job_manager/tests/test_api.py`
- `jules_job_manager/tests/conftest.py`

**Technical Notes:**
- Use `fastapi.testclient.TestClient`
- Use pytest fixtures for test app and database
- Test both success and error paths
- Verify response schemas match Pydantic models

---

### Phase 5: Testing (Week 5)

#### JJM-044: Async Operations Support
**Title:** Convert synchronous operations to async where beneficial

**Description:**
Refactor key operations to use async/await for better performance and concurrency.

**Acceptance Criteria:**
- [ ] MCP client methods converted to async
- [ ] Job manager methods converted to async
- [ ] Database operations use async SQLAlchemy
- [ ] CLI commands updated to use asyncio.run()
- [ ] Backward compatibility maintained
- [ ] Performance improvement measured and documented

**Dependencies:** JJM-031

**Estimated Effort:** 12 hours

**Phase:** Production Phase 5: Testing

**Files to Create/Modify:**
- `jules_job_manager/src/mcp_client.py`
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/src/db_storage.py`
- `jules_job_manager/src/main.py`

**Technical Notes:**
- Use `asyncio` for async operations
- Use `aiohttp` for async HTTP if needed
- Use `asyncpg` or SQLAlchemy async for database
- Convert subprocess communication to async
- Use `asyncio.gather()` for concurrent operations

---

#### JJM-045: Integration Test Suite
**Title:** Create comprehensive integration test suite

**Description:**
Build integration tests that test complete workflows with real MCP server and database.

**Acceptance Criteria:**
- [ ] Docker Compose setup for test environment (MCP server, PostgreSQL, Redis)
- [ ] Integration tests for all major workflows
- [ ] Tests can run in CI/CD pipeline
- [ ] Test data cleanup after each test
- [ ] Performance benchmarks included
- [ ] Tests marked with `@pytest.mark.integration`

**Dependencies:** JJM-031, JJM-034

**Estimated Effort:** 10 hours

**Phase:** Production Phase 5: Testing

**Files to Create/Modify:**
- `jules_job_manager/tests/integration/test_workflows.py`
- `jules_job_manager/tests/docker-compose.test.yml`
- `jules_job_manager/tests/integration/conftest.py`

**Technical Notes:**
- Use docker-compose for test services
- Use pytest-docker-compose plugin
- Test: create task → monitor → approve → complete workflow
- Measure end-to-end latency
- Clean up test tasks after completion

---

#### JJM-046: Performance Testing
**Title:** Create performance and load tests

**Description:**
Build performance tests to measure system behavior under load and identify bottlenecks.

**Acceptance Criteria:**
- [ ] Load testing script created (using locust or similar)
- [ ] Tests for concurrent task creation
- [ ] Tests for concurrent task queries
- [ ] Tests for API endpoint performance
- [ ] Performance baselines documented
- [ ] Bottlenecks identified and documented
- [ ] Performance regression tests in CI

**Dependencies:** JJM-039, JJM-040

**Estimated Effort:** 8 hours

**Phase:** Production Phase 5: Testing

**Files to Create/Modify:**
- `jules_job_manager/tests/performance/locustfile.py`
- `jules_job_manager/tests/performance/test_performance.py`
- `jules_job_manager/docs/performance_baselines.md`

**Technical Notes:**
- Use locust for load testing
- Test scenarios: 10, 50, 100 concurrent users
- Measure: response time, throughput, error rate
- Target: <200ms p95 latency for API calls
- Document resource usage (CPU, memory, database connections)

---

#### JJM-047: End-to-End Testing
**Title:** Create end-to-end tests for complete user scenarios

**Description:**
Build end-to-end tests that simulate real user workflows from CLI and API.

**Acceptance Criteria:**
- [ ] E2E tests for CLI workflows
- [ ] E2E tests for API workflows
- [ ] Tests use real MCP server (or high-fidelity mock)
- [ ] Tests verify data persistence across operations
- [ ] Tests verify error recovery
- [ ] Tests can run in CI/CD
- [ ] Test reports generated

**Dependencies:** JJM-043, JJM-045

**Estimated Effort:** 8 hours

**Phase:** Production Phase 5: Testing

**Files to Create/Modify:**
- `jules_job_manager/tests/e2e/test_cli_workflows.py`
- `jules_job_manager/tests/e2e/test_api_workflows.py`
- `jules_job_manager/tests/e2e/conftest.py`

**Technical Notes:**
- Use subprocess to test CLI commands
- Use requests library to test API
- Verify database state after operations
- Test error scenarios and recovery
- Generate HTML test reports with pytest-html

---

### Phase 6: Monitoring & Metrics (Week 6)

#### JJM-048: Prometheus Metrics Implementation
**Title:** Implement Prometheus metrics collection

**Description:**
Add Prometheus metrics for monitoring application performance and health.

**Acceptance Criteria:**
- [ ] prometheus-client library added to requirements
- [ ] Metrics endpoint `/metrics` implemented
- [ ] Counters for: tasks_created, tasks_completed, errors_total
- [ ] Histograms for: task_duration, api_request_duration
- [ ] Gauges for: active_tasks, database_connections
- [ ] Metrics labeled appropriately (operation, status, error_type)
- [ ] Metrics documented

**Dependencies:** JJM-038

**Estimated Effort:** 6 hours

**Phase:** Production Phase 6: Monitoring & Metrics

**Files to Create/Modify:**
- `jules_job_manager/src/metrics.py`
- `jules_job_manager/src/api/main.py`
- `jules_job_manager/src/job_manager.py`
- `jules_job_manager/requirements.txt`

**Technical Notes:**
- Reference plan section 2.7
- Use `prometheus_client.Counter`, `Histogram`, `Gauge`
- Expose metrics on separate port (default: 9090)
- Use decorators for automatic metric collection
- Include exemplars for tracing integration

**Blocks:** JJM-049, JJM-050, JJM-051

---

#### JJM-049: Health Check System
**Title:** Implement comprehensive health check system

**Description:**
Create health check system that monitors all dependencies and reports system health.

**Acceptance Criteria:**
- [ ] Health check for MCP server connectivity
- [ ] Health check for database connectivity
- [ ] Health check for Redis connectivity
- [ ] Health check for disk space
- [ ] `/health` endpoint returns detailed status
- [ ] `/health/live` endpoint for liveness probe
- [ ] `/health/ready` endpoint for readiness probe
- [ ] Health checks run periodically in background

**Dependencies:** JJM-048

**Estimated Effort:** 5 hours

**Phase:** Production Phase 6: Monitoring & Metrics

**Files to Create/Modify:**
- `jules_job_manager/src/health.py`
- `jules_job_manager/src/api/routes/health.py`

**Technical Notes:**
- Health check response format: `{"status": "healthy", "checks": {...}}`
- Each check returns: status (healthy/unhealthy), latency, message
- Liveness: basic app responsiveness
- Readiness: all dependencies available
- Run checks every 30 seconds in background thread

---

#### JJM-050: Alerting Configuration
**Title:** Set up alerting rules and integrations

**Description:**
Configure alerting for critical errors and system issues with integration to notification systems.

**Acceptance Criteria:**
- [ ] Alert rules defined for: high error rate, task failures, service unavailability
- [ ] Prometheus alerting rules created
- [ ] Integration with notification systems (email, Slack, PagerDuty)
- [ ] Alert severity levels defined (warning, critical)
- [ ] Alert documentation created
- [ ] Test alerts can be triggered

**Dependencies:** JJM-048

**Estimated Effort:** 6 hours

**Phase:** Production Phase 6: Monitoring & Metrics

**Files to Create/Modify:**
- `jules_job_manager/config/alerts.yml`
- `jules_job_manager/src/alerting.py`
- `jules_job_manager/docs/alerting.md`

**Technical Notes:**
- Use Prometheus Alertmanager for alert routing
- Alert on: error_rate > 5%, task_failure_rate > 10%, service_down
- Include runbooks in alert annotations
- Test with `amtool` command

---

#### JJM-051: Grafana Dashboard
**Title:** Create Grafana dashboard for monitoring

**Description:**
Build Grafana dashboard for visualizing metrics and system health.

**Acceptance Criteria:**
- [ ] Grafana dashboard JSON created
- [ ] Panels for: task throughput, error rates, latency percentiles
- [ ] Panels for: active tasks, database connections, cache hit rate
- [ ] Panels for: system resources (CPU, memory)
- [ ] Dashboard variables for filtering (time range, environment)
- [ ] Dashboard documented with screenshots

**Dependencies:** JJM-048

**Estimated Effort:** 5 hours

**Phase:** Production Phase 6: Monitoring & Metrics

**Files to Create/Modify:**
- `jules_job_manager/config/grafana_dashboard.json`
- `jules_job_manager/docs/monitoring.md`

**Technical Notes:**
- Use Prometheus as data source
- Include SLO/SLI panels (availability, latency, error rate)
- Add annotations for deployments
- Export dashboard as JSON for version control

---


