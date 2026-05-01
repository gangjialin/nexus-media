"""V1 API 路由"""

from fastapi import APIRouter

from app.api.v1 import auth, users, projects, scripts, assets, reviews, tasks, notifications, search

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(projects.router, prefix="/projects", tags=["项目"])
router.include_router(scripts.router, prefix="/scripts", tags=["剧本"])
router.include_router(assets.router, prefix="/assets", tags=["素材"])
router.include_router(reviews.router, prefix="/reviews", tags=["审阅"])
router.include_router(tasks.router, prefix="/tasks", tags=["任务"])
router.include_router(notifications.router, prefix="/notifications", tags=["通知"])
router.include_router(search.router, prefix="/search", tags=["搜索"])
