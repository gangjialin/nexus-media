"""剧本接口"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter()


class ScriptResponse(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    status: str
    current_version: int
    total_scenes: int
    created_by: UUID
    created_at: str


class SceneResponse(BaseModel):
    id: UUID
    scene_number: str
    title: Optional[str]
    location: Optional[str]
    status: str
    assigned_team_id: Optional[UUID]


# ==================== 剧本 CRUD ====================

@router.get("", response_model=list[ScriptResponse])
async def list_scripts(
    project_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
):
    """剧本列表"""
    # TODO: 实现剧本列表
    return []


@router.post("/import", response_model=ScriptResponse, status_code=status.HTTP_201_CREATED)
async def import_script(
    project_id: UUID,
    file: UploadFile = File(...),
):
    """导入剧本文件（PDF/Word/Markdown）"""
    # TODO: 实现剧本导入
    pass


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: UUID):
    """剧本详情"""
    # TODO: 实现剧本详情
    pass


# ==================== 版本管理 ====================

@router.get("/{script_id}/versions")
async def list_script_versions(script_id: UUID):
    """版本列表"""
    # TODO: 实现版本列表
    return []


@router.get("/{script_id}/versions/{version_id}/diff")
async def compare_versions(script_id: UUID, version_id: UUID, compare_to: UUID = Query(...)):
    """版本对比"""
    # TODO: 实现版本对比
    return {}


# ==================== 场景 ====================

@router.get("/{script_id}/scenes", response_model=list[SceneResponse])
async def list_scenes(script_id: UUID):
    """场景列表"""
    # TODO: 实现场景列表
    return []


@router.post("/{script_id}/scenes/{scene_id}/assign")
async def assign_scene(script_id: UUID, scene_id: UUID, team_id: UUID):
    """分配场景到制作组"""
    # TODO: 实现场景分配
    pass


# ==================== 批注 ====================

@router.get("/{script_id}/annotations")
async def list_annotations(script_id: UUID, scene_id: Optional[UUID] = Query(None)):
    """剧本批注列表"""
    # TODO: 实现批注列表
    return []


@router.post("/{script_id}/annotations", status_code=status.HTTP_201_CREATED)
async def create_annotation(script_id: UUID):
    """添加批注"""
    # TODO: 实现添加批注
    pass
