import { useEffect, useState, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { useScriptStore } from "@/stores/scriptStore";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import {
  ArrowLeft,
  MessageSquare,
  CheckCircle2,
  Circle,
  ChevronRight,
  Send,
  X,
  Quote,
} from "lucide-react";

const statusConfig: Record<string, { label: string; variant: "default" | "success" | "warning" | "secondary" }> = {
  pending: { label: "待处理", variant: "secondary" },
  in_progress: { label: "修改中", variant: "warning" },
  resolved: { label: "已修改", variant: "default" },
  confirmed: { label: "已确认", variant: "success" },
};

export function ScriptDetailPage() {
  const { id } = useParams<{ id: string }>();
  const {
    currentScript,
    scenes,
    annotations,
    loading,
    fetchScript,
    fetchScenes,
    fetchAnnotations,
    createAnnotation,
    updateAnnotation,
  } = useScriptStore();

  const [activeScene, setActiveScene] = useState<string | null>(null);
  const [showAnnotations, setShowAnnotations] = useState(false);
  const [selectionToolbar, setSelectionToolbar] = useState<{
    x: number;
    y: number;
    text: string;
  } | null>(null);
  const [commentInput, setCommentInput] = useState("");
  const [showCommentInput, setShowCommentInput] = useState(false);

  const contentRef = useRef<HTMLDivElement>(null);
  const popupRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (id) {
      fetchScript(id);
      fetchScenes(id);
      fetchAnnotations(id);
    }
  }, [id, fetchScript, fetchScenes, fetchAnnotations]);

  // 文本选择处理
  const handleTextSelect = useCallback(() => {
    // 如果已经有批注输入框打开，忽略新的选择
    if (showCommentInput) return;

    const selection = window.getSelection();
    if (!selection || selection.isCollapsed || !selection.toString().trim()) {
      return;
    }

    // 如果点击发生在批注弹窗内，忽略
    if (popupRef.current?.contains(selection.anchorNode?.parentElement)) {
      return;
    }

    const text = selection.toString().trim();
    if (text.length > 500) return;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    setSelectionToolbar({
      x: rect.left + rect.width / 2,
      y: rect.bottom + 4,
      text,
    });
  }, [showCommentInput]);

  // 关闭选择工具栏
  const clearSelection = useCallback(() => {
    setSelectionToolbar(null);
    setShowCommentInput(false);
    setCommentInput("");
    window.getSelection()?.removeAllRanges();
  }, []);

  // 提交批注
  const handleSubmitAnnotation = async () => {
    if (!commentInput.trim() || !id || !selectionToolbar) return;
    try {
      await createAnnotation(id, {
        content: commentInput,
        quote_text: selectionToolbar.text,
        scene_id: activeScene || undefined,
      });
      setCommentInput("");
      setShowCommentInput(false);
      setSelectionToolbar(null);
      window.getSelection()?.removeAllRanges();
    } catch (e) {
      alert("批注提交失败: " + (e instanceof Error ? e.message : "未知错误"));
    }
  };

  // 场景点击跳转
  const scrollToScene = (sceneId: string) => {
    setActiveScene(sceneId);
    const el = document.getElementById(`scene-${sceneId}`);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  // 渲染正文（高亮被批注的段落）
  const renderContent = () => {
    if (!currentScript?.raw_content) {
      return (
        <div className="text-center py-20 text-gray-400">
          <p>暂无剧本内容</p>
        </div>
      );
    }

    const paragraphs = currentScript.raw_content.split("\n");

    return (
      <div className="font-serif text-[15px] leading-8 text-gray-800 space-y-1">
        {paragraphs.map((para, i) => {
          // 场景标题高亮
          const isSceneTitle = /^#{1,3}\s/.test(para) || /^第?\d+场/.test(para);
          // 角色名高亮
          const isCharacter = /^【.+?】/.test(para.trim()) || /^[A-Za-z一-龥]+[：:]/.test(para.trim()) && para.trim().length < 30;
          // 动作描述
          const isAction = /^（.+?）/.test(para.trim()) || /^\(.+?\)/.test(para.trim());

          let className = "";
          if (isSceneTitle) {
            className = "text-lg font-bold text-indigo-700 mt-6 mb-2";
          } else if (isCharacter) {
            className = "font-bold text-gray-900 mt-3";
          } else if (isAction) {
            className = "text-gray-500 italic text-sm pl-4";
          } else if (para.trim() === "") {
            className = "h-2";
          }

          // 场景标题加锚点
          let anchorId = "";
          if (isSceneTitle) {
            const sceneNum = para.match(/(\d+)/)?.[1];
            if (sceneNum && scenes[parseInt(sceneNum) - 1]) {
              anchorId = scenes[parseInt(sceneNum) - 1].id;
            }
          }

          return (
            <p key={i} className={className} id={anchorId ? `scene-${anchorId}` : undefined}>
              {para || " "}
            </p>
          );
        })}
      </div>
    );
  };

  if (loading && !currentScript) {
    return (
      <div className="space-y-4 max-w-4xl">
        <Skeleton className="h-6 w-48" />
        <Skeleton className="h-4 w-32" />
        <div className="grid grid-cols-[200px_1fr] gap-6 mt-8">
          <Skeleton className="h-96" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }

  if (!currentScript) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-400">剧本不存在</p>
        <Link to="/scripts">
          <Button variant="link">返回剧本列表</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-3rem)] flex flex-col page-enter">
      {/* Header */}
      <div className="flex items-center justify-between shrink-0 mb-4">
        <div className="flex items-center gap-4">
          <Link to="/scripts">
            <Button variant="ghost" size="icon" className="text-gray-400">
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-lg font-bold text-gray-900">
              {currentScript.title}
            </h1>
            <p className="text-xs text-gray-400">
              v{currentScript.current_version} · {currentScript.total_scenes} 场
              · {currentScript.word_count?.toLocaleString() || 0} 字
              {currentScript.author ? ` · ${currentScript.author}` : ""}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge
            variant={
              currentScript.status === "published"
                ? "success"
                : currentScript.status === "reviewing"
                ? "default"
                : "secondary"
            }
          >
            {currentScript.status === "published"
              ? "已定稿"
              : currentScript.status === "reviewing"
              ? "审阅中"
              : currentScript.status === "draft"
              ? "草稿"
              : "编辑中"}
          </Badge>
          <Button
            variant={showAnnotations ? "default" : "outline"}
            size="sm"
            onClick={() => setShowAnnotations(!showAnnotations)}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            批注
            {annotations.length > 0 && (
              <span className="ml-1 text-xs">({annotations.length})</span>
            )}
          </Button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex gap-4 flex-1 min-h-0">
        {/* Scene Sidebar */}
        <Card className="w-48 shrink-0 overflow-hidden border-0 shadow-sm">
          <div className="p-3 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-50">
            场景列表
          </div>
          <div className="overflow-y-auto h-full pb-4">
            {scenes.length === 0 ? (
              <p className="text-xs text-gray-300 text-center py-8">暂无场景</p>
            ) : (
              scenes.map((scene) => (
                <button
                  key={scene.id}
                  onClick={() => scrollToScene(scene.id)}
                  className={`w-full text-left px-3 py-2 text-sm transition-colors ${
                    activeScene === scene.id
                      ? "bg-indigo-50 text-indigo-700 font-medium border-r-2 border-indigo-500"
                      : "text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <span className="text-xs font-mono text-gray-400">
                    S{scene.scene_number.padStart(2, "0")}
                  </span>
                  <span className="ml-2 text-xs truncate block">
                    {scene.title || scene.location || `场景 ${scene.scene_number}`}
                  </span>
                </button>
              ))
            )}
          </div>
        </Card>

        {/* Script Content */}
        <Card
          className="flex-1 border-0 shadow-sm"
          style={{ overflow: "visible" }}
          ref={contentRef}
        >
          <div
            className="h-full overflow-y-auto p-8"
            onMouseUp={handleTextSelect}
          >
            {renderContent()}

            {/* 选中文字后的浮动工具栏 */}
            {selectionToolbar && !showCommentInput && (
              <div
                className="fixed z-50 flex gap-1"
                style={{
                  left: selectionToolbar.x,
                  top: selectionToolbar.y - 36,
                  transform: "translateX(-50%)",
                }}
              >
                <Button
                  size="sm"
                  className="h-7 text-xs shadow-lg bg-white text-gray-700 border hover:bg-gray-50"
                  onClick={() => setShowCommentInput(true)}
                >
                  <MessageSquare className="w-3 h-3" />
                  批注
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-7 w-7 p-0 shadow-lg bg-white"
                  onClick={clearSelection}
                >
                  <X className="w-3 h-3" />
                </Button>
              </div>
            )}

            {/* 批注输入框 */}
            {showCommentInput && selectionToolbar && (
              <div
                ref={popupRef}
                className="fixed z-50 w-80"
                style={{
                  left: Math.min(selectionToolbar.x - 160, window.innerWidth - 340),
                  top: Math.max(selectionToolbar.y - 200, 60),
                }}
                onMouseDown={(e) => e.stopPropagation()}
                onMouseUp={(e) => e.stopPropagation()}
              >
                <Card className="shadow-xl border-2 border-indigo-200 p-3 space-y-2">
                  <div className="flex items-start gap-2">
                    <Quote className="w-3.5 h-3.5 text-gray-400 mt-0.5 shrink-0" />
                    <p className="text-xs text-gray-500 italic leading-relaxed line-clamp-2">
                      "{selectionToolbar.text}"
                    </p>
                  </div>
                  <textarea
                    className="w-full text-sm border border-gray-200 rounded-lg p-2 h-20 resize-none focus:outline-none focus:ring-1 focus:ring-indigo-400"
                    placeholder="输入批注内容..."
                    value={commentInput}
                    onChange={(e) => setCommentInput(e.target.value)}
                    autoFocus
                    onMouseDown={(e) => e.stopPropagation()}
                  />
                  <div className="flex justify-end gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={clearSelection}
                    >
                      取消
                    </Button>
                    <Button
                      size="sm"
                      onClick={handleSubmitAnnotation}
                      disabled={!commentInput.trim()}
                    >
                      <Send className="w-3 h-3" />
                      提交
                    </Button>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </Card>

        {/* Annotations Panel */}
        {showAnnotations && (
          <Card className="w-80 shrink-0 overflow-hidden border-0 shadow-sm">
            <div className="p-3 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-50 flex items-center justify-between">
              <span>批注列表</span>
              <Badge variant="secondary" className="text-[10px]">
                {annotations.length}
              </Badge>
            </div>
            <div className="overflow-y-auto h-full pb-4">
              {annotations.length === 0 ? (
                <div className="text-center py-12 px-4">
                  <MessageSquare className="w-8 h-8 text-gray-200 mx-auto mb-2" />
                  <p className="text-xs text-gray-400">暂无批注</p>
                  <p className="text-xs text-gray-300 mt-1">
                    选中剧本中的文字添加批注
                  </p>
                </div>
              ) : (
                <div className="divide-y divide-gray-50">
                  {annotations.map((ann) => {
                    const cfg = statusConfig[ann.status] || statusConfig.pending;
                    return (
                      <div key={ann.id} className="p-3 space-y-2 hover:bg-gray-50/50">
                        <div className="flex items-center justify-between">
                          <Badge variant={cfg.variant} className="text-[10px]">
                            {cfg.label}
                          </Badge>
                          <span className="text-[10px] text-gray-300">
                            {ann.created_at?.slice(0, 10)}
                          </span>
                        </div>
                        {ann.quote_text && (
                          <p className="text-xs text-gray-400 italic leading-relaxed bg-gray-50 p-2 rounded border-l-2 border-gray-200">
                            "{ann.quote_text}"
                          </p>
                        )}
                        <p className="text-xs text-gray-700 leading-relaxed">
                          {ann.content}
                        </p>
                        <div className="flex gap-1 pt-1">
                          {ann.status === "pending" && (
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-6 text-[10px] text-indigo-600"
                              onClick={() => updateAnnotation(ann.id, "resolved")}
                            >
                              <CheckCircle2 className="w-3 h-3" />
                              标记完成
                            </Button>
                          )}
                          {ann.status === "resolved" && (
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-6 text-[10px] text-green-600"
                              onClick={() => updateAnnotation(ann.id, "confirmed")}
                            >
                              <CheckCircle2 className="w-3 h-3" />
                              确认通过
                            </Button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
