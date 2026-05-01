import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Film } from "lucide-react";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Login:", email, password);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-indigo-50 to-purple-50">
      <div className="w-full max-w-sm mx-auto">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl mx-auto mb-5 shadow-lg shadow-indigo-200">
            <Film className="w-7 h-7" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Nexus Media</h1>
          <p className="text-sm text-gray-500 mt-1">
            AI 影视媒体资产管理系统
          </p>
        </div>

        {/* Login Card */}
        <Card className="border-0 shadow-lg shadow-gray-200/50">
          <CardContent className="p-6 space-y-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-gray-700">
                  邮箱
                </label>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  required
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-gray-700">
                  密码
                </label>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>
              <Button type="submit" className="w-full">
                登录
              </Button>
            </form>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-100" />
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="bg-white px-2 text-gray-300">开发模式</span>
              </div>
            </div>

            <Button
              variant="outline"
              className="w-full text-gray-400"
              onClick={() => {
                localStorage.setItem("access_token", "dev");
                window.location.reload();
              }}
            >
              Dev Login（跳过登录）
            </Button>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-gray-300 mt-6">
          Nexus Media v0.1.0
        </p>
      </div>
    </div>
  );
}
