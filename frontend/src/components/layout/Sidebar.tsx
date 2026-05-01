import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  FolderOpen,
  MessageSquare,
  CheckSquare,
  LogOut,
  UserCog,
} from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { useState } from "react";
import { useAuthStore, ROLE_NAMES } from "@/stores/authStore";
import type { UserRole } from "@/types";

const navItems = [
  { to: "/", icon: LayoutDashboard, label: "总控台" },
  { to: "/scripts", icon: FileText, label: "剧本管理" },
  { to: "/assets", icon: FolderOpen, label: "资产库" },
  { to: "/reviews", icon: MessageSquare, label: "审阅中心" },
  { to: "/tasks", icon: CheckSquare, label: "我的任务" },
];

export function Sidebar() {
  const [collapsed] = useState(false);
  const { user, switchRole } = useAuthStore();

  const roles: UserRole[] = ["director", "lead", "member", "producer"];
  const roleLabel = user ? ROLE_NAMES[user.role] : "导演";
  const initials = roleLabel.slice(0, 1);

  return (
    <aside
      className={`bg-white border-r border-gray-200 flex flex-col transition-all duration-200 ${
        collapsed ? "w-16" : "w-60"
      }`}
    >
      {/* Logo */}
      <div className="px-4 py-5 flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
          N
        </div>
        {!collapsed && (
          <div className="overflow-hidden">
            <h1 className="text-sm font-semibold text-gray-900 leading-tight">
              Nexus Media
            </h1>
            <p className="text-[10px] text-gray-400 leading-tight">
              影视资产管理系统
            </p>
          </div>
        )}
      </div>

      <Separator />

      {/* Nav */}
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                isActive
                  ? "bg-indigo-50 text-indigo-700"
                  : "text-gray-500 hover:bg-gray-50 hover:text-gray-900"
              }`
            }
          >
            <item.icon className="w-4 h-4 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Bottom */}
      <div className="px-2 py-3 border-t border-gray-100">
        <div className="flex items-center gap-3 px-3 py-2">
          <Avatar className="w-7 h-7">
            <AvatarFallback>{initials}</AvatarFallback>
          </Avatar>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-900 truncate">
                {roleLabel}
              </p>
              <p className="text-[10px] text-gray-400 truncate">{user?.role}</p>
            </div>
          )}
        </div>

        {/* Role Switcher (Dev Mode) */}
        {!collapsed && (
          <div className="px-3 pb-2">
            <div className="flex items-center gap-1 text-[10px] text-gray-400 mb-1">
              <UserCog className="w-3 h-3" />
              切换角色
            </div>
            <Select
              className="h-7 text-xs"
              value={user?.role || "director"}
              onChange={(e) => switchRole(e.target.value as UserRole)}
              options={roles.map((r) => ({ value: r, label: ROLE_NAMES[r] }))}
            />
          </div>
        )}

        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start text-gray-400 hover:text-gray-600 mt-1"
          onClick={() => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("dev_role");
            window.location.reload();
          }}
        >
          <LogOut className="w-3.5 h-3.5" />
          {!collapsed && <span className="text-xs">退出</span>}
        </Button>
      </div>
    </aside>
  );
}
