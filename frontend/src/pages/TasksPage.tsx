import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckSquare, Clock, CheckCircle2, AlertCircle, ListTodo } from "lucide-react";

const stats = [
  { label: "待处理", value: "5", icon: Clock, color: "text-amber-600", bg: "bg-amber-50" },
  { label: "进行中", value: "3", icon: ListTodo, color: "text-blue-600", bg: "bg-blue-50" },
  { label: "已完成", value: "12", icon: CheckCircle2, color: "text-emerald-600", bg: "bg-emerald-50" },
];

const tasks = [
  {
    title: "S02 角色动画制作",
    project: "追光者",
    deadline: "05/05",
    priority: "high" as const,
    status: "in_progress" as const,
  },
  {
    title: "S01 场景合成",
    project: "追光者",
    deadline: "05/03",
    priority: "medium" as const,
    status: "pending" as const,
  },
  {
    title: "S03 火车站渲染",
    project: "追光者",
    deadline: "05/10",
    priority: "low" as const,
    status: "pending" as const,
  },
  {
    title: "S05 BGM 混音调整",
    project: "暗夜追踪",
    deadline: "05/02",
    priority: "urgent" as const,
    status: "in_progress" as const,
  },
];

const priorityConfig = {
  urgent: { label: "紧急", variant: "destructive" as const },
  high: { label: "高", variant: "destructive" as const },
  medium: { label: "中", variant: "warning" as const },
  low: { label: "低", variant: "secondary" as const },
};

const statusConfig = {
  pending: { label: "待处理", variant: "secondary" as const },
  in_progress: { label: "进行中", variant: "default" as const },
  completed: { label: "已完成", variant: "success" as const },
};

export function TasksPage() {
  return (
    <div className="space-y-6 page-enter max-w-6xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">我的任务</h1>
        <p className="text-sm text-gray-500 mt-1">查看和处理分配给你的所有任务</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {stats.map((stat) => (
          <Card key={stat.label} className="border-0 shadow-sm">
            <CardContent className="p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500 font-medium">{stat.label}</p>
                  <p className={`text-2xl font-bold mt-1 ${stat.color}`}>{stat.value}</p>
                </div>
                <div className={`p-3 rounded-xl ${stat.bg}`}>
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Task List */}
      <Card className="border-0 shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-semibold">任务列表</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-gray-50">
            {tasks.map((task, i) => {
              const pc = priorityConfig[task.priority];
              const sc = statusConfig[task.status];
              return (
                <div
                  key={i}
                  className="flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50/80 cursor-pointer transition-colors"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {task.title}
                    </p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {task.project} · 截止 {task.deadline}
                    </p>
                  </div>
                  <Badge variant={sc.variant} className="shrink-0">
                    {sc.label}
                  </Badge>
                  <Badge variant={pc.variant} className="shrink-0">
                    {pc.label}
                  </Badge>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
