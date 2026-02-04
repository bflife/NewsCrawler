<template>
  <div class="history-list">
    <h3>爬取历史记录</h3>
    
    <div class="table-container">
      <table class="history-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>新闻源</th>
            <th>状态</th>
            <th>文章数</th>
            <th>耗时(秒)</th>
            <th>爬取时间</th>
            <th>错误信息</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in history" :key="item.id">
            <td>{{ item.id }}</td>
            <td>
              <strong>{{ item.source_id }}</strong>
            </td>
            <td>
              <span :class="['status-badge', item.status]">
                <span v-if="item.status === 'success'">✓ 成功</span>
                <span v-else>✗ 失败</span>
              </span>
            </td>
            <td class="article-count">{{ item.articles_count }}</td>
            <td>{{ item.duration_seconds.toFixed(2) }}</td>
            <td>{{ formatTime(item.crawl_time) }}</td>
            <td class="error-message">
              {{ item.error_message || '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="history.length === 0" class="empty-state">
      暂无爬取记录
    </div>
  </div>
</template>

<script setup lang="ts">
import type { History } from '@/types/scheduler';

defineProps<{
  history: History[];
}>();

function formatTime(time: string): string {
  const date = new Date(time);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}
</script>

<style scoped>
.history-list h3 {
  margin-bottom: 20px;
  color: #333;
}

.table-container {
  overflow-x: auto;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.history-table thead {
  background: #fafafa;
}

.history-table th,
.history-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e8e8e8;
}

.history-table th {
  font-weight: 600;
  color: #333;
}

.history-table tbody tr:hover {
  background: #f5f5f5;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.success {
  background: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.status-badge.failed {
  background: #fff1f0;
  color: #ff4d4f;
  border: 1px solid #ffccc7;
}

.article-count {
  font-weight: 600;
  color: #1890ff;
}

.error-message {
  max-width: 300px;
  color: #ff4d4f;
  font-size: 12px;
  word-break: break-word;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}
</style>
