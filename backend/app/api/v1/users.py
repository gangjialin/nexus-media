"""用户接口"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter()


class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: str
    role: str
    avatar_url: Optional[str] = None


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """获取当前用户信息"""
    # TODO: 从 JWT Token 获取当前用户
    raise HTTPException(status_code=401, detail="Not authenticated")


@router.put("/me", response_model=UserResponse)
async def update_current_user(update: UserUpdate):
    """更新当前用户信息"""
    # TODO: 实现用户更新
    pass


@router.get("", response_model=list[UserResponse])
async def list_users():
    """用户列表（管理员）"""
    # TODO: 实现用户列表
    return []
