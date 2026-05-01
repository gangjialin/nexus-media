export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">项目总控台</h1>
        <p className="text-sm text-gray-500 mt-1">全局项目进度概览</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "整体进度", value: "80%", color: "bg-green-500" },
          { label: "待审阅", value: "12", color: "bg-amber-500" },
          { label: "阻塞任务", value: "3", color: "bg-red-500" },
          { label: "进行中", value: "8", color: "bg-blue-500" },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl border border-gray-200 p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">{stat.label}</span>
              <div className={`w-2 h-2 rounded-full ${stat.color}`} />
            </div>
            <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* 进度总览 */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-base font-semibold text-gray-900 mb-4">按组进度</h2>
        <div className="space-y-3">
          {[
            { name: "A组 - 动画组", progress: 85, people: 8 },
            { name: "B组 - 特效组", progress: 55, people: 6 },
            { name: "C组 - 剪辑组", progress: 25, people: 4 },
          ].map((group) => (
            <div key={group.name} className="flex items-center gap-4">
              <span className="text-sm text-gray-600 w-32">{group.name}</span>
              <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-500 rounded-full transition-all"
                  style={{ width: `${group.progress}%` }}
                />
              </div>
              <span className="text-sm font-medium text-gray-700 w-12 text-right">
                {group.progress}%
              </span>
              <span className="text-xs text-gray-400 w-8">{group.people}人</span>
            </div>
          ))}
        </div>
      </div>

      {/* 最近动态 */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-base font-semibold text-gray-900 mb-4">最近动态</h2>
        <div className="space-y-3">
          {[
            { time: "10:23", text: "B组小李提交了「S03-场景合成 v2」", tag: "待组长审阅" },
            { time: "09:45", text: "张导批注了「S01-最终调色」", tag: "2条新意见" },
            { time: "09:30", text: "A组组长分配了「S02-角色动画」给小王", tag: "已分配" },
          ].map((event, i) => (
            <div key={i} className="flex items-center gap-3 text-sm">
              <span className="text-gray-400 text-xs w-10">{event.time}</span>
              <span className="text-gray-700 flex-1">{event.text}</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600">
                {event.tag}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
