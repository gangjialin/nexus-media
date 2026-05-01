export function ReviewsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">审阅中心</h1>
        <p className="text-sm text-gray-500 mt-1">
          待审阅的资产和审阅历史
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {[
          { label: "待审阅", value: "12", color: "text-amber-600" },
          { label: "已通过", value: "45", color: "text-green-600" },
          { label: "未处理批注", value: "8", color: "text-red-600" },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl border border-gray-200 p-4">
            <p className="text-sm text-gray-500">{stat.label}</p>
            <p className={`text-2xl font-bold mt-1 ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        <div className="px-4 py-3 border-b border-gray-100">
          <h2 className="text-sm font-semibold text-gray-900">待审阅列表</h2>
        </div>
        <div className="divide-y divide-gray-100">
          {[
            { name: "S03-合成-v2.mp4", submitter: "小李", group: "B组", date: "04/30" },
            { name: "S01-调色-v3.mp4", submitter: "小王", group: "A组", date: "04/29" },
          ].map((item) => (
            <div
              key={item.name}
              className="px-4 py-3 flex items-center justify-between hover:bg-gray-50 cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded bg-gray-100 flex items-center justify-center text-gray-400 text-xs">
                  🎬
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">{item.name}</p>
                  <p className="text-xs text-gray-500">
                    {item.submitter} · {item.group} · {item.date}
                  </p>
                </div>
              </div>
              <span className="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700">
                待审阅
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
