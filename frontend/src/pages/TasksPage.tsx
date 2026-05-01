export function TasksPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">我的任务</h1>
        <p className="text-sm text-gray-500 mt-1">查看和处理分配给你的所有任务</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {[
          { label: "待处理", value: "5", color: "text-amber-600" },
          { label: "进行中", value: "3", color: "text-blue-600" },
          { label: "已完成", value: "12", color: "text-green-600" },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl border border-gray-200 p-4">
            <p className="text-sm text-gray-500">{stat.label}</p>
            <p className={`text-2xl font-bold mt-1 ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        <div className="px-4 py-3 border-b border-gray-100">
          <h2 className="text-sm font-semibold text-gray-900">任务列表</h2>
        </div>
        <div className="divide-y divide-gray-100">
          {[
            { task: "S02 角色动画制作", project: "追光者", deadline: "05/05", priority: "高" },
            { task: "S01 场景合成", project: "追光者", deadline: "05/03", priority: "中" },
          ].map((item) => (
            <div
              key={item.task}
              className="px-4 py-3 flex items-center justify-between hover:bg-gray-50 cursor-pointer"
            >
              <div>
                <p className="text-sm font-medium text-gray-900">{item.task}</p>
                <p className="text-xs text-gray-500">
                  {item.project} · 截止 {item.deadline}
                </p>
              </div>
              <span
                className={`text-xs px-2 py-0.5 rounded-full ${
                  item.priority === "高"
                    ? "bg-red-50 text-red-700"
                    : "bg-amber-50 text-amber-700"
                }`}
              >
                {item.priority}优先级
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
