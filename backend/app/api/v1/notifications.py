"""通知接口"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID

router = APIRouter()


@router.get("")
async def list_notifications(page: int = Query(1), page_size: int = Query(20)):
    """通知列表"""
    # TODO: 实现通知列表
    return []


@router.put("/{notification_id}/read")
async def mark_read(notification_id: UUID):
    """标记已读"""
    # TODO: 实现标记已读
    pass


@router.put("/read-all")
async def mark_all_read():
    """全部已读"""
    # TODO: 实现全部已读
    pass


@router.get("/unread-count")
async def get_unread_count():
    """未读数"""
    return {"count": 0}
