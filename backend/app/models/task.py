"""任务模型"""

from sqlalchemy import String, Text, Integer, Date, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base
from app.models.mixins import UUIDMixin, TimestampMixin


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    LEAD_REVIEW = "lead_review"
    DIRECTOR_REVIEW = "director_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAUSED = "paused"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(UUIDMixin, TimestampMixin, Base):
    """制作任务"""
    __tablename__ = "tasks"

    project_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    scene_id: Mapped[str | None] = mapped_column(String(36))
    asset_id: Mapped[str | None] = mapped_column(String(36))
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    assigned_by: Mapped[str | None] = mapped_column(String(36))
    assigned_to: Mapped[str | None] = mapped_column(String(36), index=True)
    team_id: Mapped[str | None] = mapped_column(String(36))
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status", create_constraint=True),
        default=TaskStatus.PENDING,
    )
    priority: Mapped[Priority] = mapped_column(
        SAEnum(Priority, name="priority", create_constraint=True),
        default=Priority.MEDIUM,
    )
    due_date: Mapped[str | None] = mapped_column(Date)
    total_comments: Mapped[int] = mapped_column(default=0)
    resolved_comments: Mapped[int] = mapped_column(default=0)
