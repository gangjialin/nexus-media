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

DEV_USERS = {
    "dev": {"id": "00000000-0000-4000-8000-000000000001", "name": "开发用户", "role": UserRole.DIRECTOR},
    "dev-director": {"id": "00000000-0000-4000-8000-000000000001", "name": "张导", "role": UserRole.DIRECTOR},
    "dev-lead": {"id": "00000000-0000-4000-8000-000000000002", "name": "李组长", "role": UserRole.LEAD},
    "dev-member": {"id": "00000000-0000-4000-8000-000000000003", "name": "小王", "role": UserRole.MEMBER},
    "dev-producer": {"id": "00000000-0000-4000-8000-000000000004", "name": "赵制片", "role": UserRole.PRODUCER},
}


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取当前登录用户

    开发模式：无 token 时返回一个虚拟导演用户。
    支持 dev-{role} 格式的 token 切换角色。
    生产模式：必须有效 JWT token。
    """
    # 开发模式
    token = credentials.credentials if credentials else None
    dev_info = DEV_USERS.get(token or "", DEV_USERS.get("dev")) if token and token.startswith("dev") else (DEV_USERS.get("dev") if not token else None)

    if dev_info:
        result = await db.execute(select(User).where(User.id == dev_info["id"]))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(
                id=dev_info["id"],
                email=f"{dev_info['name']}@nexus.local",
                display_name=dev_info["name"],
                role=dev_info["role"],
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
