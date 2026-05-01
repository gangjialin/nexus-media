"""素材业务逻辑"""

from uuid import uuid4
from typing import Optional

from sqlalchemy import select, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset, AssetTag


class AssetService:
    """素材管理服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_assets(
        self,
        project_id: str,
        asset_type: Optional[str] = None,
        scene_id: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Asset], int]:
        """素材列表（支持筛选和搜索）"""
        query = select(Asset).where(
            Asset.project_id == project_id,
            Asset.status != "deleted",
        )

        if asset_type:
            query = query.where(Asset.asset_type == asset_type)
        if scene_id:
            query = query.where(Asset.scene_id == scene_id)
        if search:
            query = query.where(Asset.filename.ilike(f"%{search}%"))

        # 总数
        count_query = select(Asset.id).where(
            Asset.project_id == project_id,
            Asset.status != "deleted",
        )
        total_result = await self.db.execute(count_query)
        total = len(total_result.all())

        # 分页
        query = query.order_by(desc(Asset.created_at)).offset(
            (page - 1) * page_size
        ).limit(page_size)

        result = await self.db.execute(query)
        return list(result.scalars().all()), total
