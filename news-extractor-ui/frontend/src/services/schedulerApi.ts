/**
 * 调度器 API 服务
 */
import axios from 'axios';
import type { Task, History, Article, Stats, SchedulerStatus, CountryStats } from '@/types/scheduler';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const schedulerApi = {
  // 调度器状态
  async getStatus(): Promise<SchedulerStatus> {
    const response = await api.get<SchedulerStatus>('/api/scheduler/status');
    return response.data;
  },

  async start(): Promise<{ message: string; running: boolean }> {
    const response = await api.post('/api/scheduler/start');
    return response.data;
  },

  async stop(): Promise<{ message: string; running: boolean }> {
    const response = await api.post('/api/scheduler/stop');
    return response.data;
  },

  // 统计信息
  async getStats(): Promise<Stats> {
    const response = await api.get<Stats>('/api/scheduler/stats');
    return response.data;
  },

  // 任务管理
  async getTasks(params?: {
    country?: string;
    enabled?: boolean;
    page?: number;
    page_size?: number;
  }): Promise<Task[]> {
    const response = await api.get<Task[]>('/api/tasks', { params });
    return response.data;
  },

  async getTask(sourceId: string): Promise<Task> {
    const response = await api.get<Task>(`/api/tasks/${sourceId}`);
    return response.data;
  },

  async updateTask(sourceId: string, data: {
    enabled?: boolean;
    interval_minutes?: number;
  }): Promise<{ message: string; source_id: string }> {
    const response = await api.patch(`/api/tasks/${sourceId}`, data);
    return response.data;
  },

  async runTask(sourceId: string): Promise<{ message: string; source_id: string }> {
    const response = await api.post(`/api/tasks/${sourceId}/run`);
    return response.data;
  },

  // 国家列表
  async getCountries(): Promise<{ countries: CountryStats[] }> {
    const response = await api.get('/api/countries');
    return response.data;
  },

  // 历史记录
  async getHistory(params?: {
    source_id?: string;
    status?: 'success' | 'failed';
    limit?: number;
  }): Promise<History[]> {
    const response = await api.get<History[]>('/api/history', { params });
    return response.data;
  },

  // 文章列表
  async getArticles(params: {
    source_id: string;
    limit?: number;
  }): Promise<Article[]> {
    const response = await api.get<Article[]>('/api/articles', { params });
    return response.data;
  },

  // 初始化任务
  async initTasks(intervalMinutes: number = 60): Promise<{
    message: string;
    total_tasks: number;
    interval_minutes: number;
  }> {
    const response = await api.post('/api/init', null, {
      params: { interval_minutes: intervalMinutes }
    });
    return response.data;
  },
};
