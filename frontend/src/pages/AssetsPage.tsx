import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FolderOpen, Upload, Search, Film, Music, Image, FileType } from "lucide-react";

const mockAssets = [
  { name: "S03_合成_v2.mp4", type: "video", duration: "00:45", uploader: "李组长", date: "04/29", tags: ["S03", "合成"] },
  { name: "S01_原始素材.mov", type: "video", duration: "03:20", uploader: "小王", date: "04/28", tags: ["S01", "原始"] },
  { name: "S05_BGM_主旋律.wav", type: "audio", duration: "02:15", uploader: "李组长", date: "04/27", tags: ["S05", "BGM"] },
  { name: "概念图_车站_v3.png", type: "image", size: "4K", uploader: "美术组", date: "04/26", tags: ["概念图"] },
  { name: "剧本_v8_定稿.pdf", type: "document", size: "2.3MB", uploader: "张导", date: "04/25", tags: ["剧本", "定稿"] },
  { name: "S01_调色_V2.mp4", type: "video", duration: "00:30", uploader: "颜色组", date: "04/24", tags: ["S01", "调色"] },
];

const typeConfig: Record<string, { icon: typeof Film; color: string; bg: string }> = {
  video: { icon: Film, color: "text-blue-600", bg: "bg-blue-50" },
  audio: { icon: Music, color: "text-emerald-600", bg: "bg-emerald-50" },
  image: { icon: Image, color: "text-purple-600", bg: "bg-purple-50" },
  document: { icon: FileType, color: "text-amber-600", bg: "bg-amber-50" },
};

export function AssetsPage() {
  return (
    <div className="space-y-6 page-enter max-w-6xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">资产库</h1>
          <p className="text-sm text-gray-500 mt-1">
            集中管理视频、音频、图片等所有媒体素材
          </p>
        </div>
        <Button>
          <Upload className="w-4 h-4" />
          上传素材
        </Button>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input placeholder="搜索资产..." className="pl-9" />
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-3 gap-4">
        {mockAssets.map((asset, i) => {
          const cfg = typeConfig[asset.type] || typeConfig.document;
          const Icon = cfg.icon;
          return (
            <Card
              key={i}
              className="border-0 shadow-sm hover:shadow-md cursor-pointer transition-all duration-200 hover:-translate-y-0.5 overflow-hidden group"
            >
              {/* Preview Area */}
              <div className={`aspect-video ${cfg.bg} flex items-center justify-center relative`}>
                <Icon className={`w-10 h-10 ${cfg.color} opacity-30 group-hover:opacity-50 transition-opacity`} />
                {asset.duration && (
                  <span className="absolute bottom-2 right-2 text-xs bg-black/60 text-white px-1.5 py-0.5 rounded font-mono">
                    {asset.duration}
                  </span>
                )}
                {asset.size && (
                  <span className="absolute bottom-2 right-2 text-xs bg-black/60 text-white px-1.5 py-0.5 rounded">
                    {asset.size}
                  </span>
                )}
              </div>
              <CardContent className="p-3 space-y-2">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {asset.name}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-400">
                  <span>{asset.uploader}</span>
                  <span>{asset.date}</span>
                </div>
                <div className="flex gap-1 flex-wrap">
                  {asset.tags.map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-[10px] px-1.5 py-0">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
