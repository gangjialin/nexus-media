/** 剧本管理状态 */

import { create } from "zustand";
import { api } from "@/utils/api";
import type { Script, Scene } from "@/types";

interface ScriptState {
  scripts: Script[];
  currentScript: Script | null;
  scenes: Scene[];
  loading: boolean;
  error: string | null;

  fetchScripts: (projectId?: string, status?: string) => Promise<void>;
  fetchScript: (scriptId: string) => Promise<void>;
  fetchScenes: (scriptId: string) => Promise<void>;
  importScript: (projectId: string, file: File) => Promise<Script>;
}

export const useScriptStore = create<ScriptState>((set, get) => ({
  scripts: [],
  currentScript: null,
  scenes: [],
  loading: false,
  error: null,

  fetchScripts: async (projectId, status) => {
    set({ loading: true, error: null });
    try {
      const data = await api.get<Script[]>("/scripts", { project_id: projectId, status });
      set({ scripts: data, loading: false });
    } catch (e: any) {
      set({ error: e.message, loading: false });
    }
  },

  fetchScript: async (scriptId) => {
    set({ loading: true, error: null });
    try {
      const script = await api.get<Script>(`/scripts/${scriptId}`);
      set({ currentScript: script, loading: false });
    } catch (e: any) {
      set({ error: e.message, loading: false });
    }
  },

  fetchScenes: async (scriptId) => {
    try {
      const scenes = await api.get<Scene[]>(`/scripts/${scriptId}/scenes`);
      set({ scenes });
    } catch (e: any) {
      set({ error: e.message });
    }
  },

  importScript: async (projectId, file) => {
    set({ loading: true, error: null });
    // 使用 FormData 上传文件
    const formData = new FormData();
    formData.append("file", file);
    formData.append("project_id", projectId);

    const token = localStorage.getItem("access_token");
    const headers: Record<string, string> = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch("/api/v1/scripts/import", {
      method: "POST",
      headers,
      body: formData,
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.detail || "导入失败");
    }

    const script: Script = await response.json();
    // 刷新列表
    const { scripts } = get();
    set({ scripts: [script, ...scripts], loading: false });
    return script;
  },
}));
