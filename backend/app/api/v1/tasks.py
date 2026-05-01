"""任务接口"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

router = APIRouter()


class TaskCreate(BaseModel):
    project_id: UUID
    scene_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    assigned_to: UUID
    due_date: Optional[date] = None
    priority: str = "medium"


@router.get("/my")
async def get_my_tasks(status: Optional[str] = Query(None)):
    """我的任务"""
    # TODO: 实现我的任务
    return []


@router.get("")
async def list_tasks(
    project_id: Optional[UUID] = Query(None),
    team_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
):
    """任务列表"""
    # TODO: 实现任务列表
    return []


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """创建任务"""
    # TODO: 实现创建任务
    pass


@router.get("/{task_id}")
async def get_task(task_id: UUID):
    """任务详情"""
    # TODO: 实现任务详情
    pass


@router.put("/{task_id}")
async def update_task(task_id: UUID):
    """更新任务"""
    # TODO: 实现任务更新
    pass


@router.post("/{task_id}/submit")
async def submit_task(task_id: UUID):
    """提交任务（组员 → 组长）"""
    # TODO: 实现任务提交
    pass


@router.post("/{task_id}/claim")
async def claim_task(task_id: UUID):
    """认领任务"""
    # TODO: 实现任务认领
    pass
