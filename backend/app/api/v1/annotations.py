"""批注增强接口 — 回复链 + 确认 + 导演介入"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.script import ScriptAnnotation, AnnotationStatus

router = APIRouter()


class ReplyCreate(BaseModel):
    content: str


class AnnotationDetailResponse(BaseModel):
    id: str
    script_id: str
    scene_id: Optional[str] = None
    author_id: str
    assignee_id: Optional[str] = None
    status: str
    content: str
    quote_text: Optional[str] = None
    parent_id: Optional[str] = None
    created_at: Optional[str] = None
    replies: list["AnnotationDetailResponse"] = []

    class Config:
        from_attributes = True


# ==================== 回复批注 ====================

@router.post("/{annotation_id}/reply", status_code=status.HTTP_201_CREATED)
async def reply_to_annotation(
    annotation_id: str,
    body: ReplyCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """回复批注（组长回复组员，或导演介入）"""
    result = await db.execute(
        select(ScriptAnnotation).where(ScriptAnnotation.id == annotation_id)
    )
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status_code=404, detail="批注不存在")

    # 创建回复
    reply = ScriptAnnotation(
        script_id=annotation.script_id,
        scene_id=annotation.scene_id,
        parent_id=annotation_id,
        author_id=user.id,
        content=body.content,
        status=AnnotationStatus.IN_PROGRESS,
    )
    db.add(reply)

    # 更新原批注状态
    annotation.status = AnnotationStatus.IN_PROGRESS
    await db.commit()
    await db.refresh(reply)

    return {
        "id": reply.id,
        "parent_id": annotation_id,
        "content": reply.content,
        "author_id": reply.author_id,
        "status": reply.status.value,
        "created_at": reply.created_at.isoformat() if reply.created_at else None,
    }


# ==================== 确认批注 ====================

@router.post("/{annotation_id}/confirm")
async def confirm_annotation(
    annotation_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """组员确认已理解"""
    result = await db.execute(
        select(ScriptAnnotation).where(ScriptAnnotation.id == annotation_id)
    )
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status_code=404, detail="批注不存在")

    annotation.status = AnnotationStatus.CONFIRMED
    await db.commit()

    return {
        "id": annotation.id,
        "status": "confirmed",
    }


# ==================== 获取批注（含回复链） ====================

@router.get("", response_model=list[AnnotationDetailResponse])
async def get_annotations_threaded(
    script_id: str,
    scene_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """获取批注列表（含回复链）"""
    query = select(ScriptAnnotation).where(
        ScriptAnnotation.script_id == script_id,
        ScriptAnnotation.parent_id == None,  # 只查顶层批注
    )
    if scene_id:
        query = query.where(ScriptAnnotation.scene_id == scene_id)
    query = query.order_by(desc(ScriptAnnotation.created_at))

    result = await db.execute(query)
    top_annotations = result.scalars().all()

    # 查回复
    all_ids = [a.id for a in top_annotations]
    if all_ids:
        result = await db.execute(
            select(ScriptAnnotation)
            .where(ScriptAnnotation.parent_id.in_(all_ids))
            .order_by(ScriptAnnotation.created_at)
        )
        replies = result.scalars().all()

        # 按 parent_id 分组
        replies_map = {}
        for r in replies:
            replies_map.setdefault(r.parent_id, []).append(r)

        # 构建返回
        output = []
        for a in top_annotations:
            d = AnnotationDetailResponse(
                id=a.id,
                script_id=a.script_id,
                scene_id=a.scene_id,
                author_id=a.author_id,
                assignee_id=a.assignee_id,
                status=a.status.value if a.status else "pending",
                content=a.content,
                quote_text=a.quote_text,
                parent_id=a.parent_id,
                created_at=a.created_at.isoformat() if a.created_at else None,
                replies=[
                    AnnotationDetailResponse(
                        id=r.id,
                        script_id=r.script_id,
                        scene_id=r.scene_id,
                        author_id=r.author_id,
                        status=r.status.value if r.status else "pending",
                        content=r.content,
                        created_at=r.created_at.isoformat() if r.created_at else None,
                    )
                    for r in replies_map.get(a.id, [])
                ],
            )
            output.append(d)
        return output

    return []
