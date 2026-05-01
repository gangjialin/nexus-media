# Nexus Media — AI 影视媒体资产管理系统

> 基于 AI 驱动的智能影视媒体资产管理平台

## 项目概述

**Nexus Media** 是一个面向影视制作团队和媒体机构的智能资产管理系统，利用 AI 技术对海量媒体资产（视频、音频、图片、文档）进行自动化的分析、分类、检索和分发管理。

### 核心功能

| 模块 | 功能 |
|------|------|
| **智能入库** | 自动检测上传文件类型、编码格式、分辨率，提取技术元数据 |
| **AI 分析** | 场景识别、人脸/物体检测、语音转文字、字幕生成、智能标签 |
| **语义搜索** | 基于自然语言描述搜索画面、台词、场景 — "穿红色衣服的人在雨中奔跑" |
| **版本管理** | 素材版本追踪、剪辑时间线关联、变更历史 |
| **自动化转码** | 根据分发目标自动转码为 H.264 / H.265 / ProRes 等格式 |
| **协作审阅** | 在线预览、时间轴标注、批注、审核流 |
| **权限管理** | 基于角色的访问控制 (RBAC)、项目级隔离、水印保护 |
| **AI 智能推荐** | 根据剪辑内容推荐匹配素材、BGM、特效模板 |

## 项目结构

```
nexus-media/
├── backend/                  # 后端服务 (Python FastAPI)
│   ├── app/
│   │   ├── api/             # API 路由层
│   │   ├── core/            # 配置、中间件、依赖注入
│   │   ├── models/          # 数据模型 (SQLAlchemy)
│   │   └── services/        # 业务逻辑层
│   └── tests/               # 单元测试 / 集成测试
├── frontend/                 # 前端应用 (React / TypeScript)
│   ├── src/
│   │   ├── components/      # 通用组件
│   │   ├── pages/           # 页面组件
│   │   ├── stores/          # 状态管理
│   │   └── utils/           # 工具函数
│   └── public/              # 静态资源
├── ai/                       # AI 引擎
│   ├── models/              # 预训练模型 / 模型微调
│   ├── pipelines/           # 推理流水线 (场景检测、OCR、ASR...)
│   ├── analysis/            # 分析服务模块
│   └── indexing/            # 向量索引 (Milvus / FAISS)
├── storage/                  # 存储层
│   ├── assets/              # 原始素材文件
│   ├── thumbnails/          # 缩略图缓存
│   ├── metadata/            # 元数据导出
│   └── transcodes/          # 转码输出
├── docs/                     # 技术文档
├── scripts/                  # 部署 / 运维脚本
└── .github/workflows/        # CI/CD 流水线
```

## 技术栈

### 后端
- **框架**: Python FastAPI
- **数据库**: PostgreSQL (元数据) + Redis (缓存/队列)
- **任务队列**: Celery + RabbitMQ
- **对象存储**: MinIO / S3-compatible

### AI / ML
- **视频分析**: OpenCV, FFmpeg
- **语音识别**: Whisper (本地 / API)
- **视觉模型**: YOLO, CLIP
- **向量搜索**: Milvus / FAISS
- **NLP**: GPT 系列 / 本地 LLM (语义标签、智能描述)

### 前端
- **框架**: React + TypeScript
- **UI**: TailwindCSS + shadcn/ui
- **播放器**: Video.js / Shaka Player
- **状态管理**: Zustand

### DevOps
- **容器化**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **部署**: Nginx + Gunicorn / Uvicorn

## 快速开始

```bash
# 克隆项目
git clone <repo-url>

# 启动开发环境
docker compose up -d

# 初始化数据库
docker compose exec backend alembic upgrade head
```

## 环境要求

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- FFmpeg (AI 分析依赖)

## 许可证

MIT License
