"""FastAPI 依赖注入（认证、数据库、权限）"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, async_session
from app.core.security import decode_token
from app.models.user import User, UserRole, Team, TeamMember


security = HTTPBearer(auto_error=False)

# ==================== 开发用户体系 ====================
# 导演：张导
# 组1：组长1 → 组员1-1, 组员1-2
# 组2：组长2 → 组员2-1, 组员2-2

DEV_USERS = {
    "dev":           {"id": "dev-001", "name": "开发用户", "role": UserRole.DIRECTOR, "team": None},
    "dev-director":  {"id": "dev-001", "name": "张导",       "role": UserRole.DIRECTOR, "team": None},
    "dev-lead1":     {"id": "dev-010", "name": "组长1",      "role": UserRole.LEAD,     "team": "team-1"},
    "dev-lead2":     {"id": "dev-020", "name": "组长2",      "role": UserRole.LEAD,     "team": "team-2"},
    "dev-member11":  {"id": "dev-011", "name": "组员1-1",    "role": UserRole.MEMBER,   "team": "team-1"},
    "dev-member12":  {"id": "dev-012", "name": "组员1-2",    "role": UserRole.MEMBER,   "team": "team-1"},
    "dev-member21":  {"id": "dev-021", "name": "组员2-1",    "role": UserRole.MEMBER,   "team": "team-2"},
    "dev-member22":  {"id": "dev-022", "name": "组员2-2",    "role": UserRole.MEMBER,   "team": "team-2"},
    "dev-producer":  {"id": "dev-003", "name": "赵制片",     "role": UserRole.PRODUCER,  "team": None},
}

DEV_TEAMS = {
    "team-1": {"id": "team-1", "name": "A组 - 动画组", "type": "animation"},
    "team-2": {"id": "team-2", "name": "B组 - 特效组", "type": "vfx"},
}

# ==================== 初始化开发数据 ====================

async def init_dev_data():
    """确保开发用户和团队存在于数据库中"""
    async with async_session() as db:
        # 创建团队
        for tid, tinfo in DEV_TEAMS.items():
            result = await db.execute(select(Team).where(Team.id == tid))
            if not result.scalar_one_or_none():
                db.add(Team(id=tid, name=tinfo["name"], team_type=tinfo["type"]))

        # 创建用户 + 分配团队
        for _, uinfo in DEV_USERS.items():
            result = await db.execute(select(User).where(User.id == uinfo["id"]))
            if not result.scalar_one_or_none():
                user = User(
                    id=uinfo["id"],
                    email=f"{uinfo['name']}@nexus.local",
                    display_name=uinfo["name"],
                    role=uinfo["role"],
                    password_hash="dev",
                )
                db.add(user)

            # 加入团队
            if uinfo["team"]:
                result = await db.execute(
                    select(TeamMember).where(
                        TeamMember.team_id == uinfo["team"],
                        TeamMember.user_id == uinfo["id"],
                    )
                )
                if not result.scalar_one_or_none():
                    db.add(TeamMember(team_id=uinfo["team"], user_id=uinfo["id"]))

        await db.commit()


# ==================== 认证 ====================

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取当前登录用户

    开发模式 token 格式：
    - "dev"、"dev-director" → 张导（导演）
    - "dev-lead1"、"dev-lead2" → 组长
    - "dev-member11" 等 → 组员
    """
    await init_dev_data()

    token = credentials.credentials if credentials else None
    dev_info = None

    if not token:
        dev_info = DEV_USERS["dev"]
    elif token.startswith("dev"):
        dev_info = DEV_USERS.get(token)

    if dev_info:
        result = await db.execute(select(User).where(User.id == dev_info["id"]))
        user = result.scalar_one_or_none()
        if user:
            return user
        # fallback: create on the fly
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
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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
