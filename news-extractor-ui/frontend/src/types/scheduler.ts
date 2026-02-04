/**
 * 调度器相关类型定义
 */

export interface Task {
  id: number;
  source_id: string;
  source_name: string;
  url: string;
  country: string;
  enabled: boolean;
  interval_minutes: number;
  last_crawl_time: string | null;
  next_crawl_time: string | null;
  created_at: string;
  updated_at: string;
}

export interface History {
  id: number;
  task_id: number;
  source_id: string;
  url: string;
  status: 'success' | 'failed';
  articles_count: number;
  error_message: string | null;
  crawl_time: string;
  duration_seconds: number;
}

export interface Article {
  id: number;
  source_id: string;
  article_id: string;
  title: string;
  url: string;
  author: string | null;
  publish_time: string | null;
  summary: string | null;
  category: string | null;
  created_at: string;
}

export interface CountryStats {
  country: string;
  total_tasks: number;
  enabled_tasks: number;
  disabled_tasks: number;
}

export interface Stats {
  total_tasks: number;
  enabled_tasks: number;
  disabled_tasks: number;
  recent_success: number;
  recent_failed: number;
  countries: number;
  countries_list: CountryStats[];
}

export interface SchedulerStatus {
  running: boolean;
  registered_crawlers: number;
}
