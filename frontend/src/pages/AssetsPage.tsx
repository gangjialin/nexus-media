export function AssetsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">资产库</h1>
          <p className="text-sm text-gray-500 mt-1">
            管理所有视频、音频、图片素材
          </p>
        </div>
        <button className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700">
          上传素材
        </button>
      </div>

      {/* 筛选 */}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="搜索资产..."
          className="px-3 py-2 border border-gray-200 rounded-lg text-sm flex-1 max-w-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <select className="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white">
          <option>全部类型</option>
          <option>视频</option>
          <option>音频</option>
          <option>图片</option>
        </select>
        <select className="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white">
          <option>全部标签</option>
        </select>
      </div>

      {/* 网格视图 */}
      <div className="grid grid-cols-4 gap-4">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <div
            key={i}
            className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:border-indigo-200 cursor-pointer transition-colors"
          >
            <div className="aspect-video bg-gray-100 flex items-center justify-center text-gray-400 text-sm">
              缩略图 {i}
            </div>
            <div className="p-3">
              <p className="text-sm font-medium text-gray-900 truncate">
                S03_合成_v2.mp4
              </p>
              <p className="text-xs text-gray-500 mt-0.5">上传者 · 04/29</p>
              <div className="flex gap-1 mt-2 flex-wrap">
                <span className="text-xs px-1.5 py-0.5 rounded bg-gray-100 text-gray-600">
                  S03
                </span>
                <span className="text-xs px-1.5 py-0.5 rounded bg-gray-100 text-gray-600">
                  合成
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
