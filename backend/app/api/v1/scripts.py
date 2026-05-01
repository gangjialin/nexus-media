"""剧本接口 — 完整实现"""

import os
import tempfile
import difflib
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Form
from pydantic import BaseModel
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.script import (
    Script, ScriptVersion, Scene, ScriptAnnotation,
    ScriptStatus, SceneStatus, AnnotationStatus,
)
from app.services.script_parser import script_parser, ParsedScene
from app.services.script_service import ScriptService

router = APIRouter()


# ==================== Pydantic Schemas ====================

class ScriptResponse(BaseModel):
    id: str
    project_id: str
    title: str
    author: Optional[str]
    status: str
    current_version: int
    total_scenes: int
    word_count: int
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ScriptDetailResponse(ScriptResponse):
    raw_content: Optional[str] = None


class SceneResponse(BaseModel):
    id: str
    scene_number: str
    title: Optional[str]
    location_type: Optional[str]
    location: Optional[str]
    time_of_day: Optional[str]
    synopsis: Optional[str]
    status: str
    assigned_team_id: Optional[str]
    sort_order: Optional[int]

    class Config:
        from_attributes = True


class VersionResponse(BaseModel):
    id: str
    version_number: int
    change_log: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]

    class Config:
        from_attributes = True


class AnnotationCreate(BaseModel):
    content: str
    scene_id: Optional[str] = None
    assignee_id: Optional[str] = None
    quote_text: Optional[str] = None


class AnnotationResponse(BaseModel):
    id: str
    content: str
    quote_text: Optional[str] = None
    status: str
    author_id: str
    assignee_id: Optional[str] = None
    scene_id: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class AssignRequest(BaseModel):
    team_id: str


# ==================== 剧本 CRUD ====================

@router.get("", response_model=list[ScriptResponse])
async def list_scripts(
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """剧本列表 — 导演看全部，组长看被分配的，组员看有任务关联的"""
    service = ScriptService(db)
    scripts = await service.list_scripts(project_id=project_id, status=status)
    return [ScriptResponse.model_validate(s) for s in scripts]


@router.get("/{script_id}", response_model=ScriptDetailResponse)
async def get_script(
    script_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """剧本详情（含正文内容）"""
    service = ScriptService(db)
    script = await service.get_script(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="剧本不存在")
    return ScriptDetailResponse(
        id=script.id,
        project_id=script.project_id,
        title=script.title,
        author=script.author,
        status=script.status.value,
        current_version=script.current_version,
        total_scenes=script.total_scenes,
        word_count=script.word_count,
        raw_content=script.raw_content,
        created_by=script.created_by,
    )


@router.post("/import", response_model=ScriptResponse, status_code=status.HTTP_201_CREATED)
async def import_script(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role(UserRole.DIRECTOR, UserRole.LEAD)),
):
    """导入剧本文件（仅导演/组长可操作）

    支持格式：.md, .txt, .docx, .pdf

    流程：
    1. 保存上传文件到临时目录
    2. 用 ScriptParser 解析文件内容
    3. 创建 Script + ScriptVersion + Scene 记录
    4. 返回创建的剧本信息
    """
    # 校验文件类型
    allowed = {".md", ".txt", ".docx", ".pdf"}
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {ext}。支持: {', '.join(allowed)}",
        )

    # 保存临时文件
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # 解析剧本
        parsed = script_parser.parse(tmp_path, file.filename or "untitled")

        # 创建剧本记录
        service = ScriptService(db)
        script = await service.create_script(
            project_id=project_id,
            title=parsed.title,
            content=parsed.raw_text,
            author=parsed.author,
            created_by=user.id,
        )

        # 创建场景记录
        for i, parsed_scene in enumerate(parsed.scenes):
            scene = Scene(
                script_id=script.id,
                scene_number=parsed_scene.scene_number or str(i + 1),
                title=parsed_scene.title,
                location_type=parsed_scene.location_type,
                location=parsed_scene.location,
                time_of_day=parsed_scene.time_of_day,
                synopsis=parsed_scene.content[:500] if parsed_scene.content else None,
                sort_order=i,
            )
            db.add(scene)

        script.total_scenes = len(parsed.scenes)
        await db.commit()

        return ScriptResponse(
            id=script.id,
            project_id=script.project_id,
            title=script.title,
            author=script.author,
            status=script.status.value,
            current_version=1,
            total_scenes=script.total_scenes,
            word_count=script.word_count,
            created_by=script.created_by,
        )

    finally:
        os.unlink(tmp_path)


# ==================== 版本管理 ====================

@router.get("/{script_id}/versions", response_model=list[VersionResponse])
async def list_script_versions(
    script_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """版本列表"""
    result = await db.execute(
        select(ScriptVersion)
        .where(ScriptVersion.script_id == script_id)
        .order_by(desc(ScriptVersion.version_number))
    )
    versions = result.scalars().all()
    return [VersionResponse.model_validate(v) for v in versions]


@router.get("/{script_id}/versions/{version_id}/diff")
async def compare_versions(
    script_id: str,
    version_id: str,
    compare_to: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """版本对比：返回两个版本的差异"""
    # 获取两个版本
    result = await db.execute(
        select(ScriptVersion).where(ScriptVersion.id.in_([version_id, compare_to]))
    )
    versions = {v.id: v for v in result.scalars().all()}

    v1 = versions.get(version_id)
    v2 = versions.get(compare_to)
    if not v1 or not v2:
        raise HTTPException(status_code=404, detail="版本不存在")

    # 使用 difflib 生成差异
    diff = list(difflib.unified_diff(
        v2.content.splitlines(keepends=True),
        v1.content.splitlines(keepends=True),
        fromfile=f"v{v2.version_number}",
        tofile=f"v{v1.version_number}",
        lineterm="",
    ))

    return {
        "version_a": {"id": v1.id, "version_number": v1.version_number},
        "version_b": {"id": v2.id, "version_number": v2.version_number},
        "diff": diff,
    }


# ==================== 场景 ====================

@router.get("/{script_id}/scenes", response_model=list[SceneResponse])
async def list_scenes(
    script_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """场景列表"""
    service = ScriptService(db)
    scenes = await service.list_scenes(script_id)
    return [SceneResponse.model_validate(s) for s in scenes]


@router.post("/{script_id}/scenes/{scene_id}/assign")
async def assign_scene(
    script_id: str,
    scene_id: str,
    body: AssignRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role(UserRole.DIRECTOR)),
):
    """分配场景到制作组（仅导演可操作）"""
    service = ScriptService(db)
    scene = await service.assign_scene(scene_id, body.team_id)
    if not scene:
        raise HTTPException(status_code=404, detail="场景不存在")
    await db.commit()
    return {"status": "ok", "scene_id": scene_id, "team_id": body.team_id}


# ==================== 批注 ====================

@router.get("/{script_id}/annotations", response_model=list[AnnotationResponse])
async def list_annotations(
    script_id: str,
    scene_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """剧本批注列表"""
    service = ScriptService(db)
    annotations = await service.list_annotations(script_id, scene_id)
    return [AnnotationResponse.model_validate(a) for a in annotations]


@router.post("/{script_id}/annotations", status_code=status.HTTP_201_CREATED)
async def create_annotation(
    script_id: str,
    body: AnnotationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """添加批注"""
    service = ScriptService(db)
    annotation = await service.create_annotation(
        script_id=script_id,
        content=body.content,
        author_id=user.id,
        assignee_id=body.assignee_id,
        scene_id=body.scene_id,
        quote_text=body.quote_text,
    )
    await db.flush()
    await db.commit()

    return AnnotationResponse(
        id=annotation.id,
        content=annotation.content,
        quote_text=annotation.quote_text,
        status=annotation.status.value,
        author_id=annotation.author_id,
        assignee_id=annotation.assignee_id,
        scene_id=annotation.scene_id,
    )


class AnnotationStatusUpdate(BaseModel):
    status: str


@router.put("/annotations/{annotation_id}")
async def update_annotation_status(
    annotation_id: str,
    body: AnnotationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """更新批注状态"""
    result = await db.execute(
        select(ScriptAnnotation).where(ScriptAnnotation.id == annotation_id)
    )
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status_code=404, detail="批注不存在")

    try:
        annotation.status = AnnotationStatus(body.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效状态: {body.status}")

    await db.commit()
    return AnnotationResponse(
        id=annotation.id,
        content=annotation.content,
        quote_text=annotation.quote_text,
        status=annotation.status.value,
        author_id=annotation.author_id,
        assignee_id=annotation.assignee_id,
        scene_id=annotation.scene_id,
    )
