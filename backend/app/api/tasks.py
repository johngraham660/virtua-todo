"""
API routes for tasks.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import aiosqlite
from app.models import TaskCreate, TaskUpdate, TaskResponse
from app.database.connection import get_database

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(db: aiosqlite.Connection = Depends(get_database)):
    """Get all tasks, most recent first"""
    async with db.execute("SELECT * FROM tasks ORDER BY created_at DESC") as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db: aiosqlite.Connection = Depends(get_database)):
    """Create a new task"""
    async with db.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (task.title, task.description)
    ) as cursor:
        task_id = cursor.lastrowid
        await db.commit()
    
    # Fetch the created task
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create task")
        return dict(row)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: aiosqlite.Connection = Depends(get_database)):
    """Get a specific task"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return dict(row)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, db: aiosqlite.Connection = Depends(get_database)):
    """Update a task"""
    # Check if task exists
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
    
    # Build update query
    updates = []
    params = []
    
    if task.title is not None:
        updates.append("title = ?")
        params.append(task.title)
    
    if task.description is not None:
        updates.append("description = ?")
        params.append(task.description)
    
    if not updates:
        # No updates provided, return current task
        return dict(row)
    
    params.append(task_id)
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
    
    await db.execute(query, params)
    await db.commit()
    
    # Fetch updated task
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row)

@router.put("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int, db: aiosqlite.Connection = Depends(get_database)):
    """Mark a task as completed"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
    
    await db.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    await db.commit()
    
    # Fetch updated task
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row)

@router.put("/tasks/{task_id}/reopen", response_model=TaskResponse)
async def reopen_task(task_id: int, db: aiosqlite.Connection = Depends(get_database)):
    """Reopen a completed task"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
    
    await db.execute("UPDATE tasks SET status = 'pending' WHERE id = ?", (task_id,))
    await db.commit()
    
    # Fetch updated task
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        return dict(row)

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: aiosqlite.Connection = Depends(get_database)):
    """Delete a task"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
    
    await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await db.commit()