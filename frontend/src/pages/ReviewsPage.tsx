import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MessageSquare, Clock, CheckCircle2, AlertCircle, Film } from "lucide-react";

const stats = [
  { label: "待审阅", value: "12", icon: Clock, color: "text-amber-600", bg: "bg-amber-50" },
  { label: "已通过", value: "45", icon: CheckCircle2, color: "text-emerald-600", bg: "bg-emerald-50" },
  { label: "驳回待修改", value: "8", icon: AlertCircle, color: "text-red-600", bg: "bg-red-50" },
];

const pendingItems = [
  { name: "S03-合成-v2.mp4", submitter: "小李", group: "B组", date: "04/30", priority: "high" },
  { name: "S01-调色-v3.mp4", submitter: "小王", group: "A组", date: "04/29", priority: "medium" },
  { name: "S05-BGM-最终版.wav", submitter: "老赵", group: "声音组", date: "04/28", priority: "medium" },
  { name: "概念图_火车站_v4.png", submitter: "美术组", group: "C组", date: "04/27", priority: "low" },
];

export function ReviewsPage() {
  return (
    <div className="space-y-6 page-enter max-w-6xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">审阅中心</h1>
        <p className="text-sm text-gray-500 mt-1">审阅资产、追踪批注、确认修改</p>
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

      {/* Pending List */}
      <Card className="border-0 shadow-sm">
        <CardHeader className="pb-3 flex flex-row items-center justify-between">
          <CardTitle className="text-sm font-semibold">待审阅列表</CardTitle>
          <Badge variant="secondary">{pendingItems.length} 项</Badge>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-gray-50">
            {pendingItems.map((item, i) => (
              <div
                key={i}
                className="flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50/80 cursor-pointer transition-colors"
              >
                <div className="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center shrink-0">
                  <Film className="w-5 h-5 text-gray-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {item.name}
                  </p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {item.submitter} · {item.group} · {item.date}
                  </p>
                </div>
                <Badge
                  variant={
                    item.priority === "high"
                      ? "destructive"
                      : item.priority === "medium"
                      ? "warning"
                      : "secondary"
                  }
                  className="shrink-0"
                >
                  {item.priority === "high" ? "优先" : item.priority === "medium" ? "普通" : "低优先"}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
