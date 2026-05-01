"""素材接口"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter()


class AssetResponse(BaseModel):
    id: UUID
    filename: str
    asset_type: str
    file_size: int
    status: str
    thumbnail_url: Optional[str]
    created_by: UUID
    created_at: str


class AssetUpdate(BaseModel):
    tags: Optional[list[str]] = None
    scene_id: Optional[UUID] = None


# ==================== 资产管理 ====================

@router.get("", response_model=list[AssetResponse])
async def list_assets(
    project_id: UUID = Query(...),
    asset_type: Optional[str] = Query(None),
    scene_id: Optional[UUID] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """资产列表"""
    # TODO: 实现资产列表
    return []


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: UUID):
    """资产详情"""
    # TODO: 实现资产详情
    pass


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(asset_id: UUID, update: AssetUpdate):
    """更新资产信息"""
    # TODO: 实现资产更新
    pass


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(asset_id: UUID):
    """删除资产"""
    # TODO: 实现资产删除
    pass


# ==================== 上传 ====================

@router.post("/upload/init")
async def init_upload(filename: str, file_size: int, mime_type: str):
    """初始化上传（获取上传凭证）"""
    # TODO: 实现断点续传初始化
    return {
        "upload_id": "placeholder",
        "chunk_size": 5 * 1024 * 1024,
        "total_chunks": 0,
    }


@router.post("/upload/{upload_id}/part")
async def upload_part(upload_id: str, part_number: int, file: UploadFile = File(...)):
    """上传分片"""
    # TODO: 实现分片上传
    return {"part_number": part_number, "etag": "placeholder"}


@router.post("/upload/{upload_id}/complete")
async def complete_upload(upload_id: str):
    """完成上传"""
    # TODO: 实现上传完成
    return {"asset_id": "placeholder"}


# ==================== 预览与下载 ====================

@router.get("/{asset_id}/preview")
async def get_preview_url(asset_id: UUID):
    """获取预览信息"""
    # TODO: 返回代理文件 URL
    return {"url": "", "type": "video/mp4"}


@router.get("/{asset_id}/download")
async def download_asset(asset_id: UUID, format: Optional[str] = Query(None)):
    """下载资产"""
    # TODO: 实现文件下载
    pass


# ==================== 版本 ====================

@router.get("/{asset_id}/versions")
async def list_asset_versions(asset_id: UUID):
    """版本列表"""
    # TODO: 实现版本列表
    return []
