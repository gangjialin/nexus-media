/** 认证状态管理 */

import { create } from "zustand";
import type { User } from "@/types";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (email: string, password: string) => {
    // TODO: 实现登录 API 调用
    console.log("Login:", email, password);
    // const response = await api.post<TokenResponse>('/auth/login', { email, password });
    // localStorage.setItem('access_token', response.access_token);
    // set({ user: response.user, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem("access_token");
    set({ user: null, isAuthenticated: false });
  },

  setUser: (user: User) => {
    set({ user, isAuthenticated: true });
  },
}));
