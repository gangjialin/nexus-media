"""项目接口"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    status: str
    start_date: Optional[date]
    target_date: Optional[date]
    created_by: UUID
    created_at: str


@router.get("", response_model=list[ProjectResponse])
async def list_projects():
    """项目列表"""
    # TODO: 实现项目列表
    return []


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    """创建项目"""
    # TODO: 实现创建项目
    pass


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID):
    """项目详情"""
    # TODO: 实现项目详情
    pass


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, project: ProjectCreate):
    """更新项目"""
    # TODO: 实现更新项目
    pass


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: UUID):
    """删除项目"""
    # TODO: 实现删除项目
    pass


@router.get("/{project_id}/dashboard")
async def get_project_dashboard(project_id: UUID):
    """项目看板数据"""
    # TODO: 实现看板数据聚合
    return {"progress": {}, "teams": [], "recent_activity": []}
