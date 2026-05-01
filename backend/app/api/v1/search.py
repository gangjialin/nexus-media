"""搜索接口"""

from fastapi import APIRouter, Depends, Query
from typing import Optional

router = APIRouter()


@router.get("")
async def search(
    q: str = Query(..., min_length=1),
    project_id: Optional[str] = Query(None),
    asset_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """全局搜索"""
    # TODO: 实现全文搜索
    return {"results": [], "total": 0, "page": page, "page_size": page_size}
