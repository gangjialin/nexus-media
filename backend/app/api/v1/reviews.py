"""审阅接口"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter()


@router.get("")
async def list_reviews(status: Optional[str] = Query(None), page: int = Query(1), page_size: int = Query(20)):
    """待审阅列表"""
    # TODO: 实现审阅列表
    return []


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_review(asset_id: UUID):
    """创建审阅会话"""
    # TODO: 实现创建审阅
    pass


@router.get("/{review_id}")
async def get_review(review_id: UUID):
    """审阅详情"""
    # TODO: 实现审阅详情
    pass


@router.post("/{review_id}/comments", status_code=status.HTTP_201_CREATED)
async def add_comment(review_id: UUID):
    """添加批注"""
    # TODO: 实现添加批注
    pass


@router.get("/{review_id}/comments")
async def list_comments(review_id: UUID):
    """批注列表"""
    # TODO: 实现批注列表
    return []


@router.put("/comments/{comment_id}")
async def update_comment(comment_id: UUID):
    """更新批注状态"""
    # TODO: 实现批注状态更新
    pass


@router.post("/{review_id}/submit")
async def submit_review(review_id: UUID):
    """提交审阅意见"""
    # TODO: 实现审阅提交
    pass


@router.post("/{review_id}/approve")
async def approve_review(review_id: UUID):
    """确认通过"""
    # TODO: 实现审阅通过
    pass


@router.post("/{review_id}/reject")
async def reject_review(review_id: UUID):
    """驳回"""
    # TODO: 实现审阅驳回
    pass
