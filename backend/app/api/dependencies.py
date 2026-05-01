"""FastAPI 依赖注入（认证、数据库、权限）"""

from typing import Optional
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole


security = HTTPBearer(auto_error=False)

DEV_USER_ID = "00000000-0000-4000-8000-000000000001"


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取当前登录用户

    开发模式：无 token 时返回一个虚拟导演用户。
    生产模式：必须有效 JWT token。
    """
    # 开发模式
    if credentials is None or credentials.credentials == "dev":
        result = await db.execute(select(User).where(User.id == DEV_USER_ID))
        user = result.scalar_one_or_none()
        if user is None:
            # 创建虚拟用户
            user = User(
                id=DEV_USER_ID,
                email="dev@nexus-media.local",
                display_name="开发用户",
                role=UserRole.DIRECTOR,
                password_hash="dev",
            )
            db.add(user)
            await db.flush()
        return user

    # 生产模式：解析 JWT
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


def require_role(*roles: UserRole):
    """权限校验依赖"""

    async def checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {[r.value for r in roles]}",
            )
        return user

    return checker
