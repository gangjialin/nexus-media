"""审阅相关模型"""

from sqlalchemy import String, Text, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base
from app.models.mixins import UUIDMixin, TimestampMixin


class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class CommentStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CONFIRMED = "confirmed"


class Review(UUIDMixin, TimestampMixin, Base):
    """审阅会话"""
    __tablename__ = "reviews"

    asset_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    asset_version: Mapped[int | None] = mapped_column(Integer)
    reviewer_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[ReviewStatus] = mapped_column(
        SAEnum(ReviewStatus, name="review_status", create_constraint=True),
        default=ReviewStatus.PENDING,
    )


class ReviewComment(UUIDMixin, TimestampMixin, Base):
    """审阅批注（核心模型）"""
    __tablename__ = "review_comments"

    review_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    asset_id: Mapped[str] = mapped_column(String(36), nullable=False)
    parent_id: Mapped[str | None] = mapped_column(String(36))
    author_id: Mapped[str] = mapped_column(String(36), nullable=False)
    assignee_id: Mapped[str | None] = mapped_column(String(36))
    timestamp_ms: Mapped[int | None] = mapped_column(Integer)
    bbox: Mapped[dict | None] = mapped_column(default=dict)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    attachments: Mapped[list] = mapped_column(default=list)
    status: Mapped[CommentStatus] = mapped_column(
        SAEnum(CommentStatus, name="comment_status", create_constraint=True),
        default=CommentStatus.PENDING,
    )
