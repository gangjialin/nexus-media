import { useEffect, useState, useRef } from "react";
import { useScriptStore } from "@/stores/scriptStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { FileText, Upload, Search, Plus } from "lucide-react";

const statusConfig: Record<string, { label: string; variant: "success" | "warning" | "default" | "secondary" }> = {
  draft: { label: "草稿", variant: "secondary" },
  editing: { label: "编辑中", variant: "warning" },
  reviewing: { label: "审阅中", variant: "default" },
  published: { label: "已定稿", variant: "success" },
};

export function ScriptsPage() {
  const { scripts, loading, error, fetchScripts, importScript } = useScriptStore();
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchScripts();
  }, [fetchScripts]);

  const handleImport = async () => {
    const file = fileInputRef.current?.files?.[0];
    if (!file) return;

    const projectId = "00000000-0000-4000-8000-000000000002";
    setUploading(true);
    try {
      await importScript(projectId, file);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (e: any) {
      alert("导入失败: " + e.message);
    } finally {
      setUploading(false);
    }
  };

  const filteredScripts = scripts.filter(
    (s) =>
      s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.author?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 page-enter max-w-6xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">剧本管理</h1>
          <p className="text-sm text-gray-500 mt-1">
            导入和管理剧本，支持 PDF、Word、Markdown 格式
          </p>
        </div>
        <div className="flex gap-2">
          <input
            ref={fileInputRef}
            type="file"
            accept=".md,.txt,.docx,.pdf"
            className="hidden"
            onChange={handleImport}
          />
          <Button
            variant="outline"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            <Upload className="w-4 h-4" />
            {uploading ? "导入中..." : "导入剧本"}
          </Button>
          <Button disabled>
            <Plus className="w-4 h-4" />
            新建
          </Button>
        </div>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            placeholder="搜索剧本..."
            className="pl-9"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-100 rounded-xl text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && filteredScripts.length === 0 && (
        <Card className="border-0 shadow-sm">
          <CardContent className="flex flex-col items-center justify-center py-16">
            <div className="w-16 h-16 rounded-2xl bg-indigo-50 flex items-center justify-center mb-4">
              <FileText className="w-8 h-8 text-indigo-400" />
            </div>
            <p className="text-base font-medium text-gray-700 mb-1">
              还没有剧本
            </p>
            <p className="text-sm text-gray-400 mb-4">
              点击「导入剧本」上传第一个剧本文件
            </p>
            <Button
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="w-4 h-4" />
              导入你的第一个剧本
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Loading */}
      {loading && scripts.length === 0 && (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="border-0 shadow-sm">
              <CardContent className="p-5">
                <div className="flex items-center justify-between">
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-48" />
                    <Skeleton className="h-3 w-32" />
                  </div>
                  <Skeleton className="h-5 w-16 rounded-full" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Script List */}
      {filteredScripts.length > 0 && (
        <div className="space-y-2">
          {filteredScripts.map((script) => {
            const cfg = statusConfig[script.status] || { label: script.status, variant: "secondary" as const };
            return (
              <Card
                key={script.id}
                className="border-0 shadow-sm hover:shadow-md cursor-pointer transition-all duration-200 hover:-translate-y-0.5"
              >
                <CardContent className="p-5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 flex-1 min-w-0">
                      <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center shrink-0">
                        <FileText className="w-5 h-5 text-indigo-500" />
                      </div>
                      <div className="min-w-0">
                        <h3 className="text-sm font-semibold text-gray-900 truncate">
                          {script.title}
                        </h3>
                        <p className="text-xs text-gray-400 mt-0.5">
                          v{script.current_version}
                          {" · "}{script.total_scenes} 场
                          {" · "}{script.word_count?.toLocaleString() || 0} 字
                          {script.author ? ` · ${script.author}` : ""}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 ml-4">
                      <Badge variant={cfg.variant}>{cfg.label}</Badge>
                      <span className="text-xs text-gray-300">
                        {script.updated_at?.slice(0, 10) || script.created_at?.slice(0, 10)}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
