"""Initial database tables

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-01
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 启用扩展
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\"")

    # ==================== users ====================
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("phone", sa.String(20)),
        sa.Column("role", sa.Enum("admin", "director", "lead", "member", "producer", "external",
                                   name="user_role", create_type=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("preferences", postgresql.JSONB(), default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_users_email", "users", ["email"])

    # ==================== teams ====================
    op.create_table(
        "teams",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(500)),
        sa.Column("team_type", sa.String(50)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ==================== team_members ====================
    op.create_table(
        "team_members",
        sa.Column("team_id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), primary_key=True),
    )

    # ==================== projects ====================
    op.create_table(
        "projects",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.String(2000)),
        sa.Column("status", sa.Enum("planning", "active", "paused", "completed", "archived",
                                      name="project_status", create_type=True),
                  default="active"),
        sa.Column("start_date", sa.Date()),
        sa.Column("target_date", sa.Date()),
        sa.Column("cover_url", sa.String(500)),
        sa.Column("settings", postgresql.JSONB(), default=dict),
        sa.Column("created_by", sa.String(36)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ==================== project_teams ====================
    op.create_table(
        "project_teams",
        sa.Column("project_id", sa.String(36), primary_key=True),
        sa.Column("team_id", sa.String(36), primary_key=True),
    )

    # ==================== project_members ====================
    op.create_table(
        "project_members",
        sa.Column("project_id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), primary_key=True),
        sa.Column("role_override", sa.String(20)),
    )

    # ==================== scripts ====================
    op.create_table(
        "scripts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("author", sa.String(200)),
        sa.Column("status", sa.Enum("draft", "editing", "reviewing", "published",
                                      name="script_status", create_type=True), default="draft"),
        sa.Column("current_version", sa.Integer(), default=1),
        sa.Column("total_scenes", sa.Integer(), default=0),
        sa.Column("word_count", sa.Integer(), default=0),
        sa.Column("raw_content", sa.Text()),
        sa.Column("extra_data", postgresql.JSONB(), default=dict),
        sa.Column("created_by", sa.String(36)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_scripts_project", "scripts", ["project_id"])

    # ==================== script_versions ====================
    op.create_table(
        "script_versions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("script_id", sa.String(36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("change_log", sa.String(500)),
        sa.Column("created_by", sa.String(36)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_script_versions_script", "script_versions", ["script_id"])

    # ==================== scenes ====================
    op.create_table(
        "scenes",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("script_id", sa.String(36), nullable=False),
        sa.Column("scene_number", sa.String(10), nullable=False),
        sa.Column("title", sa.String(200)),
        sa.Column("location_type", sa.String(20)),
        sa.Column("location", sa.String(200)),
        sa.Column("time_of_day", sa.String(20)),
        sa.Column("synopsis", sa.Text()),
        sa.Column("page_start", sa.Integer()),
        sa.Column("page_end", sa.Integer()),
        sa.Column("status", sa.Enum("pending", "assigned", "in_progress", "lead_review",
                                      "director_review", "completed",
                                      name="scene_status", create_type=True), default="pending"),
        sa.Column("assigned_team_id", sa.String(36)),
        sa.Column("sort_order", sa.Integer()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_scenes_script", "scenes", ["script_id"])

    # ==================== script_annotations ====================
    op.create_table(
        "script_annotations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("script_id", sa.String(36), nullable=False),
        sa.Column("scene_id", sa.String(36)),
        sa.Column("author_id", sa.String(36), nullable=False),
        sa.Column("assignee_id", sa.String(36)),
        sa.Column("status", sa.Enum("pending", "in_progress", "resolved", "confirmed",
                                      name="annotation_status", create_type=True), default="pending"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("quote_text", sa.Text()),
        sa.Column("position_start", sa.Integer()),
        sa.Column("position_end", sa.Integer()),
        sa.Column("parent_id", sa.String(36)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_annotations_script", "script_annotations", ["script_id"])

    # ==================== assets ====================
    op.create_table(
        "assets",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("scene_id", sa.String(36)),
        sa.Column("task_id", sa.String(36)),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("original_name", sa.String(500)),
        sa.Column("file_path", sa.String(1000)),
        sa.Column("file_size", sa.BigInteger()),
        sa.Column("file_hash", sa.String(64)),
        sa.Column("mime_type", sa.String(100)),
        sa.Column("asset_type", sa.Enum("video", "audio", "image", "subtitle", "3d_model", "document",
                                         "other", name="asset_type", create_type=True), nullable=False),
        sa.Column("status", sa.Enum("uploading", "processing", "ready", "archived", "deleted",
                                      name="asset_status", create_type=True), default="uploading"),
        sa.Column("tech_metadata", postgresql.JSONB(), default=dict),
        sa.Column("thumbnail_paths", postgresql.JSONB(), default=list),
        sa.Column("proxy_status", sa.Enum("none", "pending", "processing", "ready", "failed",
                                            name="proxy_status", create_type=True), default="none"),
        sa.Column("proxy_url", sa.String(500)),
        sa.Column("ai_status", sa.Enum("none", "pending", "processing", "completed", "failed",
                                         name="ai_status", create_type=True), default="none"),
        sa.Column("ai_tags", postgresql.JSONB(), default=list),
        sa.Column("version_group", sa.String(36)),
        sa.Column("version_number", sa.Integer(), default=1),
        sa.Column("is_latest", sa.Boolean(), default=True),
        sa.Column("uploaded_by", sa.String(36)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_assets_project", "assets", ["project_id"])

    # ==================== reviews ====================
    op.create_table(
        "reviews",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("asset_id", sa.String(36), nullable=False),
        sa.Column("asset_version", sa.Integer()),
        sa.Column("reviewer_id", sa.String(36), nullable=False),
        sa.Column("status", sa.Enum("pending", "in_progress", "submitted", "approved", "rejected",
                                      name="review_status", create_type=True), default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_reviews_asset", "reviews", ["asset_id"])

    # ==================== review_comments ====================
    op.create_table(
        "review_comments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("review_id", sa.String(36), nullable=False),
        sa.Column("asset_id", sa.String(36), nullable=False),
        sa.Column("parent_id", sa.String(36)),
        sa.Column("author_id", sa.String(36), nullable=False),
        sa.Column("assignee_id", sa.String(36)),
        sa.Column("timestamp_ms", sa.Integer()),
        sa.Column("bbox", postgresql.JSONB()),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("attachments", postgresql.JSONB(), default=list),
        sa.Column("status", sa.Enum("pending", "in_progress", "resolved", "confirmed",
                                      name="comment_status", create_type=True), default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_review_comments_review", "review_comments", ["review_id"])

    # ==================== tasks ====================
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("scene_id", sa.String(36)),
        sa.Column("asset_id", sa.String(36)),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("assigned_by", sa.String(36)),
        sa.Column("assigned_to", sa.String(36)),
        sa.Column("team_id", sa.String(36)),
        sa.Column("status", sa.Enum("pending", "in_progress", "submitted", "lead_review",
                                      "director_review", "approved", "rejected", "paused",
                                      name="task_status", create_type=True), default="pending"),
        sa.Column("priority", sa.Enum("low", "medium", "high", "urgent",
                                        name="priority", create_type=True), default="medium"),
        sa.Column("due_date", sa.Date()),
        sa.Column("total_comments", sa.Integer(), default=0),
        sa.Column("resolved_comments", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_tasks_project", "tasks", ["project_id"])
    op.create_index("idx_tasks_assigned_to", "tasks", ["assigned_to"])

    # ==================== notifications ====================
    op.create_table(
        "notifications",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("content", sa.Text()),
        sa.Column("ref_type", sa.String(50)),
        sa.Column("ref_id", sa.String(36)),
        sa.Column("is_read", sa.Boolean(), default=False),
        sa.Column("push_channels", postgresql.JSONB(), default=list),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_notifications_user", "notifications", ["user_id", "is_read"])


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("tasks")
    op.drop_table("review_comments")
    op.drop_table("reviews")
    op.drop_table("assets")
    op.drop_table("script_annotations")
    op.drop_table("scenes")
    op.drop_table("script_versions")
    op.drop_table("scripts")
    op.drop_table("project_members")
    op.drop_table("project_teams")
    op.drop_table("projects")
    op.drop_table("team_members")
    op.drop_table("teams")
    op.drop_table("users")

    # 删除枚举类型
    op.execute("DROP TYPE IF EXISTS priority CASCADE")
    op.execute("DROP TYPE IF EXISTS task_status CASCADE")
    op.execute("DROP TYPE IF EXISTS comment_status CASCADE")
    op.execute("DROP TYPE IF EXISTS review_status CASCADE")
    op.execute("DROP TYPE IF EXISTS ai_status CASCADE")
    op.execute("DROP TYPE IF EXISTS proxy_status CASCADE")
    op.execute("DROP TYPE IF EXISTS asset_status CASCADE")
    op.execute("DROP TYPE IF EXISTS asset_type CASCADE")
    op.execute("DROP TYPE IF EXISTS annotation_status CASCADE")
    op.execute("DROP TYPE IF EXISTS scene_status CASCADE")
    op.execute("DROP TYPE IF EXISTS script_status CASCADE")
    op.execute("DROP TYPE IF EXISTS project_status CASCADE")
    op.execute("DROP TYPE IF EXISTS user_role CASCADE")
