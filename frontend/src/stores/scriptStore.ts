/** 剧本管理状态 */

import { create } from "zustand";
import { api } from "@/utils/api";
import type { Script, Scene, ScriptAnnotation } from "@/types";

interface ScriptState {
  scripts: Script[];
  currentScript: Script | null;
  scenes: Scene[];
  annotations: ScriptAnnotation[];
  loading: boolean;
  error: string | null;

  fetchScripts: (projectId?: string, status?: string) => Promise<void>;
  fetchScript: (scriptId: string) => Promise<void>;
  fetchScenes: (scriptId: string) => Promise<void>;
  importScript: (projectId: string, file: File) => Promise<Script>;

  fetchAnnotations: (scriptId: string, sceneId?: string) => Promise<void>;
  createAnnotation: (scriptId: string, data: {
    content: string;
    scene_id?: string;
    assignee_id?: string;
    quote_text?: string;
  }) => Promise<void>;
  updateAnnotation: (annotationId: string, status: string) => Promise<void>;
}

export const useScriptStore = create<ScriptState>((set, get) => ({
  scripts: [],
  currentScript: null,
  scenes: [],
  annotations: [],
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
    const { scripts } = get();
    set({ scripts: [script, ...scripts], loading: false });
    return script;
  },

  // ==================== 批注 ====================

  fetchAnnotations: async (scriptId, sceneId) => {
    try {
      const data = await api.get<ScriptAnnotation[]>(`/scripts/${scriptId}/annotations`, {
        scene_id: sceneId,
      });
      set({ annotations: data });
    } catch (e: any) {
      set({ error: e.message });
    }
  },

  createAnnotation: async (scriptId, data) => {
    try {
      await api.post(`/scripts/${scriptId}/annotations`, data);
      // 刷新批注列表
      await get().fetchAnnotations(scriptId);
    } catch (e: any) {
      set({ error: e.message });
      throw e;
    }
  },

  updateAnnotation: async (annotationId, status) => {
    try {
      await api.put(`/scripts/annotations/${annotationId}`, { status } as any);
      // 刷新当前剧本的批注
      const { currentScript } = get();
      if (currentScript) {
        await get().fetchAnnotations(currentScript.id);
      }
    } catch (e: any) {
      set({ error: e.message });
    }
  },
}));
