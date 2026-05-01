export function ScriptsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">剧本管理</h1>
          <p className="text-sm text-gray-500 mt-1">
            集中管理所有剧本，支持在线阅读和批注
          </p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50">
            ＋ 新建
          </button>
          <button className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700">
            导入剧本
          </button>
        </div>
      </div>

      {/* 筛选 */}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="搜索剧本..."
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm flex-1 max-w-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <select className="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white">
          <option>全部项目</option>
        </select>
        <select className="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white">
          <option>全部状态</option>
        </select>
      </div>

      {/* 剧本列表 */}
      <div className="space-y-2">
        {[
          { title: "追光者", project: "追光者", status: "已定稿", version: "v8", scenes: 12, updated: "04/28" },
          { title: "暗夜追踪", project: "暗夜追踪", status: "编辑中", version: "v3", scenes: 8, updated: "04/30" },
        ].map((script) => (
          <div
            key={script.title}
            className="bg-white rounded-xl border border-gray-200 p-4 hover:border-indigo-200 cursor-pointer transition-colors"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold text-gray-900">
                  {script.title}
                </h3>
                <p className="text-xs text-gray-500 mt-0.5">
                  {script.project} · {script.scenes} 场 · {script.version}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`text-xs px-2 py-0.5 rounded-full ${
                    script.status === "已定稿"
                      ? "bg-green-50 text-green-700"
                      : "bg-amber-50 text-amber-700"
                  }`}
                >
                  {script.status}
                </span>
                <span className="text-xs text-gray-400">{script.updated}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
