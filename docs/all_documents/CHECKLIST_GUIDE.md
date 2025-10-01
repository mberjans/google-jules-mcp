# Jules Job Manager - Checklist Guide

This guide explains how to use the detailed task checklists for implementing the Jules Job Manager.

## 📋 Checklist Files

### 1. **`docs/checklist.md`** - MVP Tasks
Contains detailed tasks for all 25 MVP tickets (JJM-001 to JJM-025):
- **Phase 1:** Foundation (JJM-001 to JJM-005)
- **Phase 2:** Core Features (JJM-006 to JJM-009)
- **Phase 3:** Advanced Operations (JJM-010 to JJM-013)
- **Phase 4:** CLI Interface (JJM-014 to JJM-021)
- **Phase 5:** Testing & Documentation (JJM-022 to JJM-025)

### 2. **`docs/checklist_production.md`** - Production Tasks
Contains detailed tasks for production enhancement tickets (JJM-026 to JJM-037):
- **Phase 1:** Error Handling & Logging (JJM-026 to JJM-029)
- **Phase 2:** Database Integration (JJM-030 to JJM-033)
- **Phase 3:** Caching & Performance (JJM-034 to JJM-037)

**Note:** Additional production phases (JJM-038 to JJM-062) will be added as needed.

## 🎯 Task ID Format

Each task has a unique identifier in the format: **JJM-XXX-TYY**

- **JJM** = Jules Job Manager
- **XXX** = Ticket number (001-062)
- **T** = Task
- **YY** = Task number within ticket (01-99)

**Examples:**
- `JJM-001-T01` = First task of ticket JJM-001
- `JJM-014-T25` = 25th task of ticket JJM-014
- `JJM-026-T13` = 13th task of ticket JJM-026

## 🔄 Test-Driven Development (TDD) Workflow

Every feature follows the TDD cycle:

### 1. **Red Phase** - Write Failing Tests
```
- [ ] JJM-XXX-T01: Create test file
- [ ] JJM-XXX-T02: Write test for feature A
- [ ] JJM-XXX-T03: Write test for feature B
- [ ] JJM-XXX-T04: Run tests (should fail)
```

### 2. **Green Phase** - Implement Code
```
- [ ] JJM-XXX-T05: Create implementation file
- [ ] JJM-XXX-T06: Implement feature A
- [ ] JJM-XXX-T07: Implement feature B
- [ ] JJM-XXX-T08: Run tests (should pass)
```

### 3. **Refactor Phase** - Improve Code
```
- [ ] JJM-XXX-T09: Add docstrings
- [ ] JJM-XXX-T10: Add type hints
- [ ] JJM-XXX-T11: Optimize code
- [ ] JJM-XXX-T12: Run tests again
```

### 4. **Verify Phase** - Check Quality
```
- [ ] JJM-XXX-T13: Check code coverage
- [ ] JJM-XXX-T14: Review code quality
- [ ] JJM-XXX-T15: Commit changes
- [ ] JJM-XXX-T16: Push to repository
```

## 📝 Task Types

Each ticket contains various types of tasks:

### Testing Tasks
- Creating test files
- Writing unit tests
- Writing integration tests
- Running tests
- Checking code coverage

### Implementation Tasks
- Creating source files
- Implementing classes and methods
- Adding error handling
- Adding logging

### Quality Tasks
- Adding docstrings
- Adding type hints
- Code refactoring
- Performance optimization

### Documentation Tasks
- Writing README sections
- Creating usage examples
- Adding inline comments

### Git Operations
- Committing changes
- Pushing to repository
- Creating tags

## ✅ How to Use the Checklists

### For AI Coding Agents

1. **Start with JJM-001-T01** (first task of first ticket)
2. **Execute each task sequentially** within a ticket
3. **Check off completed tasks** using `[x]` instead of `[ ]`
4. **Run tests after implementation** to verify correctness
5. **Commit after each ticket** is complete
6. **Move to next ticket** only after all tasks are checked

### For Human Developers

1. **Review the entire ticket** before starting
2. **Follow TDD workflow** (Red → Green → Refactor)
3. **Check off tasks** as you complete them
4. **Run tests frequently** to catch issues early
5. **Commit with descriptive messages** referencing ticket IDs
6. **Track progress** using the checkboxes

## 🔍 Example: JJM-002 (Data Models)

Here's how the TDD workflow looks for implementing data models:

### Red Phase (Write Tests First)
```
✅ JJM-002-T01: Create jules_job_manager/tests/test_models.py
✅ JJM-002-T02: Write test for TaskStatus enum creation
✅ JJM-002-T03: Write test for TaskStatus enum values
✅ JJM-002-T04: Write test for ChatMessage dataclass initialization
...
✅ JJM-002-T15: Run tests (should fail - Red phase)
```

### Green Phase (Implement Code)
```
✅ JJM-002-T16: Create jules_job_manager/src/models.py
✅ JJM-002-T17: Implement TaskStatus enum with all values
✅ JJM-002-T18: Implement ChatMessage dataclass with type hints
...
✅ JJM-002-T25: Run tests (should pass - Green phase)
```

### Refactor Phase (Improve Quality)
```
✅ JJM-002-T26: Add docstrings to all classes and methods
✅ JJM-002-T27: Add type hints validation
✅ JJM-002-T28: Run tests again to verify refactoring
```

### Verify Phase (Check & Commit)
```
✅ JJM-002-T29: Check code coverage
✅ JJM-002-T30: Commit changes: "JJM-002: Implement data models with tests"
✅ JJM-002-T31: Push to repository
```

## 📊 Progress Tracking

### Ticket-Level Progress
Track completion of entire tickets:
- ✅ JJM-001: Project Structure Setup (20/20 tasks complete)
- ✅ JJM-002: Data Models Implementation (31/31 tasks complete)
- 🔄 JJM-003: MCP Client Foundation (15/31 tasks complete)
- ⏳ JJM-004: MCP Tool Invocation (0/37 tasks)

### Phase-Level Progress
Track completion of development phases:
- ✅ Phase 1: Foundation (5/5 tickets, 100%)
- 🔄 Phase 2: Core Features (2/4 tickets, 50%)
- ⏳ Phase 3: Advanced Operations (0/5 tickets, 0%)

### Overall Progress
Track total project completion:
- **MVP:** 25 tickets, ~600 tasks
- **Production:** 37 tickets, ~1000 tasks
- **Total:** 62 tickets, ~1600 tasks

## 🎓 Best Practices

### 1. **Always Write Tests First**
Never skip the test-writing phase. Tests are your safety net.

### 2. **Run Tests Frequently**
Run tests after every implementation task to catch issues early.

### 3. **Check Code Coverage**
Aim for >80% code coverage for all modules.

### 4. **Commit Often**
Commit after completing each ticket, not after multiple tickets.

### 5. **Use Descriptive Commit Messages**
Always reference the ticket ID in commit messages:
```bash
git commit -m "JJM-002: Implement data models with tests"
```

### 6. **Don't Skip Refactoring**
The refactor phase is crucial for code quality and maintainability.

### 7. **Document As You Go**
Add docstrings and comments during implementation, not after.

### 8. **Verify Before Moving On**
Always check code coverage and run all tests before moving to the next ticket.

## 🚀 Getting Started

### Step 1: Set Up Environment
```bash
cd jules_job_manager
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start with JJM-001
Open `docs/checklist.md` and begin with the first task:
```
- [ ] JJM-001-T01: Create root directory `jules_job_manager/`
```

### Step 3: Follow TDD Workflow
For each ticket:
1. Read all tasks in the ticket
2. Execute tasks in order
3. Check off completed tasks
4. Run tests after implementation
5. Commit when ticket is complete

### Step 4: Track Progress
Update the checklist file as you complete tasks:
```markdown
- [x] JJM-001-T01: Create root directory `jules_job_manager/`
- [x] JJM-001-T02: Create `jules_job_manager/src/` directory
- [ ] JJM-001-T03: Create `jules_job_manager/tests/` directory
```

## 📈 Milestones

### MVP Milestones
- **Milestone 1:** Foundation Complete (JJM-001 to JJM-005)
- **Milestone 2:** Core Features Complete (JJM-006 to JJM-009)
- **Milestone 3:** Advanced Operations Complete (JJM-010 to JJM-013)
- **Milestone 4:** CLI Complete (JJM-014 to JJM-021)
- **Milestone 5:** MVP Complete (JJM-022 to JJM-025)

### Production Milestones
- **Milestone 6:** Error Handling Complete (JJM-026 to JJM-029)
- **Milestone 7:** Database Integration Complete (JJM-030 to JJM-033)
- **Milestone 8:** Caching Complete (JJM-034 to JJM-037)
- **Milestone 9:** Web API Complete (JJM-038 to JJM-043)
- **Milestone 10:** Production Ready (JJM-044 to JJM-062)

## 🔧 Tools and Commands

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run only integration tests
pytest tests/ -v -m integration
```

### Code Quality
```bash
# Check code style
flake8 src/

# Type checking
mypy src/

# Format code
black src/ tests/
```

### Git Operations
```bash
# Commit with ticket reference
git commit -m "JJM-XXX: Description of changes"

# Push to repository
git push origin master

# Create tag for milestone
git tag v0.1.0-mvp
git push origin v0.1.0-mvp
```

## 📚 Related Documentation

- **`docs/tickets.md`** - Detailed ticket descriptions
- **`docs/plan.md`** - Comprehensive implementation plan
- **`docs/TICKETS_OVERVIEW.md`** - Ticket overview and summary
- **`README.md`** - Project overview

## 💡 Tips for Success

1. **Don't rush** - Take time to understand each task
2. **Read the plan** - Refer to `docs/plan.md` for implementation details
3. **Ask questions** - If a task is unclear, review the ticket description
4. **Test thoroughly** - Write comprehensive tests, not just happy paths
5. **Keep it simple** - Implement the simplest solution that passes tests
6. **Refactor confidently** - Tests give you confidence to improve code
7. **Document well** - Future you will thank present you
8. **Commit often** - Small, frequent commits are better than large ones

---

**Ready to start?** Open `docs/checklist.md` and begin with JJM-001-T01! 🚀

