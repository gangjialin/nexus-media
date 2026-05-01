/** 认证状态管理 */

import { create } from "zustand";
import type { User, UserRole } from "@/types";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  switchRole: (role: UserRole) => void;
}

const ROLE_NAMES: Record<UserRole, string> = {
  admin: "管理员",
  director: "导演",
  lead: "组长",
  member: "组员",
  producer: "制片",
  external: "外部",
};

const ROLE_IDS: Record<UserRole, string> = {
  admin: "00000000-0000-4000-8000-000000000001",
  director: "00000000-0000-4000-8000-000000000001",
  lead: "00000000-0000-4000-8000-000000000002",
  member: "00000000-0000-4000-8000-000000000003",
  producer: "00000000-0000-4000-8000-000000000004",
  external: "00000000-0000-4000-8000-000000000005",
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (_email, _password) => {
    localStorage.setItem("access_token", "dev");
    set({
      user: {
        id: ROLE_IDS.director,
        email: "director@nexus.local",
        display_name: "张导",
        role: "director",
      },
      isAuthenticated: true,
    });
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("dev_role");
    set({ user: null, isAuthenticated: false });
  },

  switchRole: (role, devToken?: string) => {
    const token = devToken || `dev-${role}`;
    localStorage.setItem("access_token", token);
    localStorage.setItem("dev_role", role);
    window.location.reload();
  },
}));

export { ROLE_NAMES };
