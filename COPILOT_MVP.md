# 📝 TODO Application — Requirements & Design Document

## 1. Purpose and Vision

The goal of this project is to create a **minimalist, distraction-free TODO application** that focuses purely on **managing tasks efficiently** — no unnecessary features, no subscriptions, and no clutter.

### Core Principles
- 🧩 Simplicity first  
- ⚡ Fast, offline-ready  
- 🔒 Privacy by design (no tracking)  
- 💾 Reliable persistence  
- 🧠 Easy to maintain and extend  

---

## 2. Target Users

- Individuals who prefer lightweight productivity tools  
- Developers and tech-savvy users who dislike bloated apps  
- Users who want offline-first, privacy-respecting software  

---

## 3. Key Features (MVP)

| Feature | Description |
|----------|-------------|
| Add Tasks | Quickly add a new TODO item |
| View Tasks | See a list of pending and completed tasks |
| Edit Tasks | Modify task titles or notes |
| Mark as Complete | Toggle a task’s status |
| Delete Tasks | Permanently remove a task |
| Persistent Storage | Tasks remain after closing/reopening the app |
| Minimalist UI | No ads, popups, or distracting visuals |

---

## 4. Future (Non-MVP) Features (Optional)

- Task prioritization (Low/Medium/High)  
- Due dates & reminders  
- Search/filtering  
- Categories or tags  
- Cross-device sync (cloud or self-hosted)  
- Keyboard shortcuts (desktop)  
- Dark/light theme toggle  
- Export/import (JSON, CSV)

---

## 5. Technical Requirements

| Area | Requirement |
|------|-------------|
| Platform | Web |
| Frontend | Svelte |
| Backend | FastAPI |
| Database | SQLite (persistent file on Kubernetes PVC) |
| Persistence | Local `.db` file backed by Persistent Volume Claim |
| UX | Clean typography, no animations, no marketing elements, must have light & dark modes |
| Accessibility | Keyboard navigation and ARIA-friendly elements |
| Deployment| ArgoCD deploys to Kubernetes with MetalLB, PVC storage on local NAS (192.168.1.200)|

---

## 6. User Stories & Acceptance Criteria

### **User Story 1: Add a new task**
> As a user, I want to quickly add a new task so that I can remember something I need to do.

**Acceptance Criteria:**
- GIVEN I am on the main screen  
  WHEN I enter text into the “New Task” field and press Enter or click “Add”  
  THEN a new task should appear in my task list.  
- WHEN the task is added  
  THEN the input field should clear automatically.  
- WHEN I refresh the app  
  THEN the new task should still appear in the list.

---

### **User Story 2: View my tasks**
> As a user, I want to see all my tasks so I can track what’s pending.

**Acceptance Criteria:**
- GIVEN I have added one or more tasks  
  WHEN I open the app  
  THEN I should see all my pending and completed tasks in a list.  
- WHEN I complete a task  
  THEN it should appear visually distinct (e.g., strikethrough or greyed out).  
- WHEN I reload the app  
  THEN all tasks should reappear with their correct status.

---

### **User Story 3: Mark a task as complete**
> As a user, I want to mark a task as done so I can keep track of my progress.

**Acceptance Criteria:**
- GIVEN I have a list of tasks  
  WHEN I click the checkbox next to a task  
  THEN the task should be marked as completed.  
- WHEN a completed task is displayed  
  THEN it should appear visually distinct from incomplete tasks.  
- WHEN I click the checkbox again  
  THEN the task should return to an incomplete state.

---

### **User Story 4: Edit a task**
> As a user, I want to edit a task in case I made a typo or want to clarify it.

**Acceptance Criteria:**
- GIVEN I have an existing task  
  WHEN I click the “edit” icon or double-click the task text  
  THEN the task should switch to edit mode.  
- WHEN I make a change and press Enter  
  THEN the updated text should replace the old one and be saved.  
- WHEN I press Escape during editing  
  THEN the task should revert to its original text without saving.

---

### **User Story 5: Delete a task**
> As a user, I want to delete a task so that I can remove irrelevant or completed items.

**Acceptance Criteria:**
- GIVEN a task exists in my list  
  WHEN I click the “delete” icon next to it  
  THEN the task should be removed from the list immediately.  
- WHEN I reload the app  
  THEN the deleted task should not reappear.

---

### **User Story 6: Persist data**
> As a user, I want my tasks to remain available after closing the app.

**Acceptance Criteria:**
- GIVEN I have created or modified tasks  
  WHEN I close and reopen the app  
  THEN all tasks should appear exactly as I left them, including completion status.  
- WHEN I clear browser data or storage  
  THEN the tasks should no longer appear (verifying persistence scope).

---

### **User Story 7: Maintain focus**
> As a user, I don’t want to be distracted by unnecessary features.

**Acceptance Criteria:**
- WHEN I use the app  
  THEN there should be no ads, popups, tooltips, or gamified elements.  
- WHEN I interact with the interface  
  THEN the visual design should remain simple, with neutral colors and readable text.  
- WHEN I perform core actions (add/edit/complete/delete)  
  THEN each should take no more than two clicks.

---

## 7. Non-Functional Requirements

| Category | Requirement |
|-----------|-------------|
| Performance | The app should load within 1 second on a typical desktop browser. |
| Reliability | Data should persist even after closing or refreshing. |
| Usability | All core actions (add, edit, complete, delete) should be doable in ≤2 clicks. |
| Privacy | No external tracking, analytics, or data sharing. |
| Portability | Should work on modern browsers (Chrome, Firefox, Safari, Edge). |

---

## 8. Success Criteria

The app is considered successful when:
- Users can add, view, edit, complete, and delete tasks without distractions.  
- The app works fully offline.  
- Data persists locally.  
- The UI feels instant, clean, and efficient.  

---

## 9. Data Persistence Design and Backup Strategy

### **Database Choice**
The app will use **SQLite** for persistent storage, aligning with the goals of simplicity, low overhead, and easy deployment in Kubernetes.

### **Database Location**
- Database file: `/app/data/todo.db`
- Stored on a **Persistent Volume Claim (PVC)** to survive Pod restarts.

### Database Schema

```sql
-- Main tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) > 0 AND length(title) <= 200),
    description TEXT CHECK(description IS NULL OR length(description) <= 1000),
    status TEXT NOT NULL CHECK(status IN ('pending', 'completed')) DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);

-- Trigger to automatically update updated_at timestamp
CREATE TRIGGER update_tasks_updated_at
    AFTER UPDATE ON tasks
    FOR EACH ROW
    WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### Schema Design Notes

**Field Constraints:**
- `title`: Required, 1-200 characters (prevents empty tasks and overly long titles)
- `description`: Optional, max 1000 characters (allows detailed notes)
- `status`: Enforced enum values to prevent invalid states
- Timestamps use SQLite's CURRENT_TIMESTAMP for consistency

**Performance Optimizations:**
- Index on `status` for filtering pending/completed tasks
- Index on `created_at DESC` to support "most recent first" ordering
- Index on `updated_at` for potential future sorting needs

**Data Integrity:**
- Primary key auto-increment ensures unique IDs
- CHECK constraints prevent invalid data
- Automatic timestamp updating via trigger
- NOT NULL constraints on required fields

**Future-Proofing:**
- Schema can easily accommodate future features like priorities, due dates, or categories
- Timestamp precision supports detailed tracking
- Description field allows rich task details without schema changes

## 10. API 

### API Data Model

| Field | Type | Description |
|--------|------|-------------|
| `id` | integer | Auto-generated unique task ID |
| `title` | string | Short title of the task (required) |
| `description` | string | Optional notes/details about the task |
| `status` | string | One of: `"pending"` or `"completed"` |
| `created_at` | string (ISO 8601) | Timestamp when the task was created |
| `updated_at` | string (ISO 8601) | Timestamp when the task was last updated |

Example JSON:
```json
{
  "id": 1,
  "title": "Buy milk",
  "description": "2% organic",
  "status": "pending",
  "created_at": "2025-11-02T13:45:00Z",
  "updated_at": "2025-11-02T13:45:00Z"
}
```

### API Endpoints

| Method   | Endpoint               | Description                                             |
| -------- | ---------------------- | ------------------------------------------------------- |
| `GET`    | `/tasks`               | Retrieve all tasks                                      |
| `POST`   | `/tasks`               | Create a new task                                       |
| `GET`    | `/tasks/{id}`          | Retrieve a single task by ID                            |
| `PUT`    | `/tasks/{id}`          | Update an existing task (title, description, or status) |
| `PATCH`  | `/tasks/{id}/complete` | Mark task as completed                                  |
| `PATCH`  | `/tasks/{id}/reopen`   | Revert task to pending                                  |
| `DELETE` | `/tasks/{id}`          | Delete a task                                           |


### Endpoint Details

1️⃣ GET /tasks

Retrieve a list of all tasks, ordered by creation date (most recent first).

Response:
```json
[
  {
    "id": 1,
    "title": "Buy milk",
    "description": "2% organic",
    "status": "pending",
    "created_at": "2025-11-02T13:45:00Z",
    "updated_at": "2025-11-02T13:45:00Z"
  },
  {
    "id": 2,
    "title": "Take out trash",
    "status": "completed",
    "created_at": "2025-11-01T08:00:00Z",
    "updated_at": "2025-11-01T09:00:00Z"
  }
]
```

Status codes:

* 200 OK — List of tasks returned successfully.


2️⃣ POST /tasks

Create a new task.

Request Body:
```json
{
  "title": "Buy milk",
  "description": "2% organic"
}
```

Response:
```json
{
  "id": 1,
  "title": "Buy milk",
  "description": "2% organic",
  "status": "pending",
  "created_at": "2025-11-02T13:45:00Z",
  "updated_at": "2025-11-02T13:45:00Z"
}
```

Status codes:

* 201 Created — Task created successfully.
* 400 Bad Request — Missing or invalid title.

3️⃣ GET /tasks/{id}

Retrieve a single task by its ID.

Response:
```json
{
  "id": 1,
  "title": "Buy milk",
  "description": "2% organic",
  "status": "pending",
  "created_at": "2025-11-02T13:45:00Z",
  "updated_at": "2025-11-02T13:45:00Z"
}
```

Status codes:

* 200 OK — Task returned successfully.
* 404 Not Found — No task found with given ID.

4️⃣ PUT /tasks/{id}

Update an existing task. This replaces the full task (title, description, status).

Request Body:
```json
{
  "title": "Buy almond milk",
  "description": "Unsweetened",
  "status": "pending"
}
```

Response:
```json
{
  "id": 1,
  "title": "Buy almond milk",
  "description": "Unsweetened",
  "status": "pending",
  "created_at": "2025-11-02T13:45:00Z",
  "updated_at": "2025-11-02T14:10:00Z"
}
```

Status codes:

* 200 OK — Task updated successfully.
* 400 Bad Request — Invalid data.
* 404 Not Found — Task not found.


5️⃣ PATCH /tasks/{id}/complete

Mark a task as completed.

Response:
```json
{
  "id": 1,
  "title": "Buy milk",
  "status": "completed",
  "updated_at": "2025-11-02T14:00:00Z"
}
```

Status codes:

* 200 OK — Task marked as completed.
* 404 Not Found — Task not found.


6️⃣ PATCH /tasks/{id}/reopen

Revert a completed task back to “pending”.

Response:
```json
{
  "id": 1,
  "title": "Buy milk",
  "status": "pending",
  "updated_at": "2025-11-02T14:05:00Z"
}
```

Status codes:

* 200 OK — Task reopened.
* 404 Not Found — Task not found.


7️⃣ DELETE /tasks/{id}

Delete a task permanently.

Response:
```json
{ "message": "Task deleted successfully" }
```

Status codes:

* 204 No Content — Task deleted.
* 404 Not Found — Task not found.

## 11. Validation Rules

### Input Validation
- `title`: Required, 1-200 characters, no HTML tags
- `description`: Optional, max 1000 characters
- `status`: Must be "pending" or "completed"

## 12. Kubernetes Deployment
- **container image**: python:3.13-slim
- **PVC**: 5GB storage for SQLlite database
- **Deployment Method**: ArgoCD