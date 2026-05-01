"""认证接口"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """用户登录"""
    # TODO: 实现真实的认证逻辑
    return TokenResponse(
        access_token="placeholder",
        refresh_token="placeholder",
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """刷新访问令牌"""
    # TODO: 实现令牌刷新逻辑
    return TokenResponse(
        access_token="placeholder",
        refresh_token="placeholder",
    )
