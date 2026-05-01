"""素材模型"""

from sqlalchemy import String, Text, Integer, BigInteger, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base
from app.models.mixins import UUIDMixin, TimestampMixin


class AssetType(str, enum.Enum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    SUBTITLE = "subtitle"
    MODEL_3D = "3d_model"
    DOCUMENT = "document"
    OTHER = "other"


class AssetStatus(str, enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ARCHIVED = "archived"
    DELETED = "deleted"


class ProxyStatus(str, enum.Enum):
    NONE = "none"
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class AIStatus(str, enum.Enum):
    NONE = "none"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Asset(UUIDMixin, TimestampMixin, Base):
    """素材"""
    __tablename__ = "assets"

    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    scene_id: Mapped[str | None] = mapped_column(String(36))
    task_id: Mapped[str | None] = mapped_column(String(36))
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[str | None] = mapped_column(String(500))
    file_path: Mapped[str | None] = mapped_column(String(1000))
    file_size: Mapped[int | None] = mapped_column(BigInteger)
    file_hash: Mapped[str | None] = mapped_column(String(64))
    mime_type: Mapped[str | None] = mapped_column(String(100))
    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(AssetType, name="asset_type", create_constraint=True),
        nullable=False,
    )
    status: Mapped[AssetStatus] = mapped_column(
        SAEnum(AssetStatus, name="asset_status", create_constraint=True),
        default=AssetStatus.UPLOADING,
    )
    tech_metadata: Mapped[dict] = mapped_column(default=dict)
    thumbnail_paths: Mapped[list] = mapped_column(default=list)
    proxy_status: Mapped[ProxyStatus] = mapped_column(
        SAEnum(ProxyStatus, name="proxy_status", create_constraint=True),
        default=ProxyStatus.NONE,
    )
    proxy_url: Mapped[str | None] = mapped_column(String(500))
    ai_status: Mapped[AIStatus] = mapped_column(
        SAEnum(AIStatus, name="ai_status", create_constraint=True),
        default=AIStatus.NONE,
    )
    ai_tags: Mapped[list] = mapped_column(default=list)
    version_group: Mapped[str | None] = mapped_column(String(36))
    version_number: Mapped[int] = mapped_column(default=1)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(36))


class AssetTag(Base):
    """素材标签"""
    __tablename__ = "asset_tags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    tag: Mapped[str] = mapped_column(String(100), nullable=False)
    tag_type: Mapped[str] = mapped_column(default="manual")
    created_by: Mapped[str | None] = mapped_column(String(36))
