import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/stores/authStore";
import {
  TrendingUp,
  Clock,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";

const stats = [
  {
    title: "整体进度",
    value: "80%",
    change: "+5.2%",
    icon: TrendingUp,
    color: "text-emerald-600",
    bg: "bg-emerald-50",
  },
  {
    title: "待审阅",
    value: "12",
    desc: "等待处理",
    icon: Clock,
    color: "text-amber-600",
    bg: "bg-amber-50",
  },
  {
    title: "阻塞任务",
    value: "3",
    desc: "需要关注",
    icon: AlertCircle,
    color: "text-red-600",
    bg: "bg-red-50",
  },
  {
    title: "已完成",
    value: "45",
    desc: "本月总计",
    icon: CheckCircle2,
    color: "text-emerald-600",
    bg: "bg-emerald-50",
  },
];

const teams = [
  { name: "A组 - 动画组", progress: 85, lead: "李组长", members: 8, color: "bg-indigo-500" },
  { name: "B组 - 特效组", progress: 55, lead: "王组长", members: 6, color: "bg-violet-500" },
  { name: "C组 - 剪辑组", progress: 25, lead: "张组长", members: 4, color: "bg-amber-500" },
];

const activities = [
  { time: "10:23", text: "B组小李提交了「S03-场景合成 v2」", type: "submit" },
  { time: "09:45", text: "张导批注了「S01-最终调色」— 2条新意见", type: "review" },
  { time: "09:30", text: "A组组长分配了「S02-角色动画」给小王", type: "assign" },
  { time: "08:15", text: "「追光者」项目进度更新至 80%", type: "update" },
];

const typeStyles = {
  submit: "bg-blue-50 text-blue-700",
  review: "bg-amber-50 text-amber-700",
  assign: "bg-violet-50 text-violet-700",
  update: "bg-emerald-50 text-emerald-700",
};

export function DashboardPage() {
  const { user } = useAuthStore();
  const roleTitle = user?.role === "director" ? "总控台"
    : user?.role === "lead" ? "组内看板"
    : user?.role === "member" ? "我的任务"
    : user?.role === "producer" ? "制片看板"
    : "总控台";
  const roleDesc = user?.role === "director" ? "全局项目进度与团队动态"
    : user?.role === "lead" ? "本组任务进度与组员状态"
    : user?.role === "member" ? "分配给我的任务"
    : user?.role === "producer" ? "项目排期与资源监控"
    : "";

  return (
    <div className="space-y-6 page-enter max-w-6xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{roleTitle}</h1>
        <p className="text-sm text-gray-500 mt-1">{roleDesc}</p>
        <Badge variant="secondary" className="mt-2 text-[10px]">
          {user?.role === "director" ? "👤 导演视图" :
           user?.role === "lead" ? "👤 组长视图" :
           user?.role === "member" ? "👤 组员视图" :
           user?.role === "producer" ? "👤 制片视图" : ""}
        </Badge>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-4">
        {stats.map((stat) => (
          <Card key={stat.title} className="border-0 shadow-sm">
            <CardContent className="p-5">
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <p className="text-xs text-gray-500 font-medium">
                    {stat.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stat.value}
                  </p>
                  {stat.change && (
                    <p className="text-xs text-emerald-600 font-medium">
                      {stat.change}
                    </p>
                  )}
                  {stat.desc && (
                    <p className="text-xs text-gray-400">{stat.desc}</p>
                  )}
                </div>
                <div className={`p-2.5 rounded-xl ${stat.bg}`}>
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Two columns */}
      <div className="grid grid-cols-3 gap-4">
        {/* Team Progress */}
        <Card className="col-span-2 border-0 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-semibold">
              按组进度
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {teams.map((team) => (
              <div key={team.name} className="space-y-1.5">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-700">
                    {team.name}
                  </span>
                  <span className="text-xs text-gray-400">
                    {team.lead} · {team.members}人
                  </span>
                </div>
                <div className="relative h-2.5 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={`absolute inset-y-0 left-0 rounded-full transition-all duration-500 ${team.color}`}
                    style={{ width: `${team.progress}%` }}
                  />
                </div>
                <div className="flex justify-between text-xs text-gray-400">
                  <span>{team.progress}% 完成</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="border-0 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-semibold">
              最近动态
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {activities.map((event, i) => (
                <div key={i} className="flex gap-3">
                  <div className="flex flex-col items-center gap-1">
                    <div className="w-1.5 h-1.5 rounded-full bg-gray-300 mt-1.5" />
                    {i < activities.length - 1 && (
                      <div className="w-px flex-1 bg-gray-100" />
                    )}
                  </div>
                  <div className="pb-2 flex-1 min-w-0">
                    <p className="text-xs text-gray-400">{event.time}</p>
                    <p className="text-sm text-gray-600 mt-0.5 leading-relaxed">
                      {event.text}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
