/** Nexus Media - TypeScript 类型定义 */

// ==================== 用户 ====================

export type UserRole =
  | "admin"
  | "director"
  | "lead"
  | "member"
  | "producer"
  | "external";

export interface User {
  id: string;
  email: string;
  display_name: string;
  role: UserRole;
  avatar_url?: string;
  phone?: string;
}

// ==================== 项目 ====================

export interface Project {
  id: string;
  name: string;
  description?: string;
  status: "planning" | "active" | "paused" | "completed" | "archived";
  start_date?: string;
  target_date?: string;
  created_by: string;
  created_at: string;
}

// ==================== 剧本 ====================

export interface Script {
  id: string;
  project_id: string;
  title: string;
  author?: string;
  status: "draft" | "editing" | "reviewing" | "published";
  current_version: number;
  total_scenes: number;
  word_count: number;
  raw_content?: string;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Scene {
  id: string;
  scene_number: string;
  title?: string;
  location?: string;
  status: string;
  assigned_team_id?: string;
}

export interface ScriptAnnotation {
  id: string;
  content: string;
  status: "pending" | "in_progress" | "resolved" | "confirmed";
  author_id: string;
  assignee_id?: string;
  created_at: string;
}

// ==================== 素材 ====================

export interface Asset {
  id: string;
  project_id: string;
  filename: string;
  asset_type: "video" | "audio" | "image" | "subtitle" | "document";
  file_size: number;
  status: string;
  thumbnail_url?: string;
  tech_metadata?: Record<string, unknown>;
  ai_tags?: string[];
  created_by: string;
  created_at: string;
}

// ==================== 审阅 ====================

export interface ReviewComment {
  id: string;
  timestamp_ms?: number;
  content: string;
  status: "pending" | "in_progress" | "resolved" | "confirmed";
  author_id: string;
  assignee_id?: string;
  bbox?: { x: number; y: number; w: number; h: number };
  created_at: string;
}

// ==================== 任务 ====================

export interface Task {
  id: string;
  project_id: string;
  title: string;
  status: string;
  priority: "low" | "medium" | "high" | "urgent";
  assigned_to?: string;
  due_date?: string;
  created_at: string;
}

// ==================== API ====================

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  meta?: {
    page: number;
    page_size: number;
    total: number;
  };
}
