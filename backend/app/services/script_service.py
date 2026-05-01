"""剧本业务逻辑"""

from uuid import uuid4
from typing import Optional

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.script import Script, ScriptVersion, Scene, ScriptAnnotation


class ScriptService:
    """剧本管理服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== 剧本 CRUD ====================

    async def create_script(self, project_id: str, title: str, content: str, created_by: str) -> Script:
        """创建剧本"""
        script = Script(
            project_id=project_id,
            title=title,
            raw_content=content,
            created_by=created_by,
        )
        self.db.add(script)
        await self.db.flush()

        # 创建初始版本
        version = ScriptVersion(
            script_id=script.id,
            version_number=1,
            content=content,
            created_by=created_by,
        )
        self.db.add(version)
        return script

    async def get_script(self, script_id: str) -> Optional[Script]:
        """获取剧本"""
        result = await self.db.execute(select(Script).where(Script.id == script_id))
        return result.scalar_one_or_none()

    async def list_scripts(self, project_id: Optional[str] = None, status: Optional[str] = None) -> list[Script]:
        """剧本列表"""
        query = select(Script)
        if project_id:
            query = query.where(Script.project_id == project_id)
        if status:
            query = query.where(Script.status == status)
        query = query.order_by(desc(Script.updated_at))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ==================== 版本管理 ====================

    async def create_version(self, script_id: str, content: str, change_log: str, created_by: str) -> ScriptVersion:
        """创建新版本（每次定稿时调用）"""
        # 获取当前最新版本号
        result = await self.db.execute(
            select(ScriptVersion)
            .where(ScriptVersion.script_id == script_id)
            .order_by(desc(ScriptVersion.version_number))
            .limit(1)
        )
        latest = result.scalar_one_or_none()
        new_version_number = (latest.version_number + 1) if latest else 1

        version = ScriptVersion(
            script_id=script_id,
            version_number=new_version_number,
            content=content,
            change_log=change_log,
            created_by=created_by,
        )
        self.db.add(version)
        return version

    # ==================== 场景管理 ====================

    async def list_scenes(self, script_id: str) -> list[Scene]:
        """场景列表"""
        result = await self.db.execute(
            select(Scene)
            .where(Scene.script_id == script_id)
            .order_by(Scene.sort_order)
        )
        return list(result.scalars().all())

    async def assign_scene(self, scene_id: str, team_id: str) -> Optional[Scene]:
        """分配场景到制作组"""
        result = await self.db.execute(select(Scene).where(Scene.id == scene_id))
        scene = result.scalar_one_or_none()
        if scene:
            scene.assigned_team_id = team_id
            scene.status = "assigned"
        return scene

    # ==================== 批注管理 ====================

    async def create_annotation(
        self,
        script_id: str,
        content: str,
        author_id: str,
        assignee_id: Optional[str] = None,
        scene_id: Optional[str] = None,
        quote_text: Optional[str] = None,
    ) -> ScriptAnnotation:
        """添加批注"""
        annotation = ScriptAnnotation(
            script_id=script_id,
            scene_id=scene_id,
            author_id=author_id,
            assignee_id=assignee_id,
            content=content,
            quote_text=quote_text,
        )
        self.db.add(annotation)
        return annotation

    async def list_annotations(self, script_id: str, scene_id: Optional[str] = None) -> list[ScriptAnnotation]:
        """批注列表"""
        query = select(ScriptAnnotation).where(ScriptAnnotation.script_id == script_id)
        if scene_id:
            query = query.where(ScriptAnnotation.scene_id == scene_id)
        query = query.order_by(desc(ScriptAnnotation.created_at))
        result = await self.db.execute(query)
        return list(result.scalars().all())
