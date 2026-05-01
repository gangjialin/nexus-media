"""剧本、场景、版本、批注模型"""

from sqlalchemy import String, Text, Integer, Enum as SAEnum, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base
from app.models.mixins import UUIDMixin, TimestampMixin


class ScriptStatus(str, enum.Enum):
    DRAFT = "draft"
    EDITING = "editing"
    REVIEWING = "reviewing"
    PUBLISHED = "published"


class SceneStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    LEAD_REVIEW = "lead_review"
    DIRECTOR_REVIEW = "director_review"
    COMPLETED = "completed"


class AnnotationStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CONFIRMED = "confirmed"


class Script(UUIDMixin, TimestampMixin, Base):
    """剧本"""
    __tablename__ = "scripts"

    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    author: Mapped[str | None] = mapped_column(String(200))
    status: Mapped[ScriptStatus] = mapped_column(
        SAEnum(ScriptStatus, name="script_status", create_constraint=True),
        default=ScriptStatus.DRAFT,
    )
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    total_scenes: Mapped[int] = mapped_column(Integer, default=0)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    raw_content: Mapped[str | None] = mapped_column(Text)
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_by: Mapped[str | None] = mapped_column(String(36))


class ScriptVersion(UUIDMixin, TimestampMixin, Base):
    """剧本版本"""
    __tablename__ = "script_versions"

    script_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    change_log: Mapped[str | None] = mapped_column(String(500))
    created_by: Mapped[str | None] = mapped_column(String(36))


class Scene(UUIDMixin, TimestampMixin, Base):
    """场景"""
    __tablename__ = "scenes"

    script_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    scene_number: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str | None] = mapped_column(String(200))
    location_type: Mapped[str | None] = mapped_column(String(20))
    location: Mapped[str | None] = mapped_column(String(200))
    time_of_day: Mapped[str | None] = mapped_column(String(20))
    synopsis: Mapped[str | None] = mapped_column(Text)
    page_start: Mapped[int | None] = mapped_column(Integer)
    page_end: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[SceneStatus] = mapped_column(
        SAEnum(SceneStatus, name="scene_status", create_constraint=True),
        default=SceneStatus.PENDING,
    )
    assigned_team_id: Mapped[str | None] = mapped_column(String(36))
    sort_order: Mapped[int | None] = mapped_column(Integer)


class ScriptAnnotation(UUIDMixin, TimestampMixin, Base):
    """剧本批注"""
    __tablename__ = "script_annotations"

    script_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    scene_id: Mapped[str | None] = mapped_column(String(36))
    author_id: Mapped[str] = mapped_column(String(36), nullable=False)
    assignee_id: Mapped[str | None] = mapped_column(String(36))
    status: Mapped[AnnotationStatus] = mapped_column(
        SAEnum(AnnotationStatus, name="annotation_status", create_constraint=True),
        default=AnnotationStatus.PENDING,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    quote_text: Mapped[str | None] = mapped_column(Text)
    position_start: Mapped[int | None] = mapped_column(Integer)
    position_end: Mapped[int | None] = mapped_column(Integer)
    parent_id: Mapped[str | None] = mapped_column(String(36))
