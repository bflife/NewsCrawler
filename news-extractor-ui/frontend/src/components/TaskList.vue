<template>
  <div class="task-list">
    <!-- 筛选器 -->
    <div class="filters">
      <div class="filter-group">
        <label>国家/地区:</label>
        <select v-model="selectedCountry" @change="filterTasks">
          <option value="">全部</option>
          <option v-for="country in countries" :key="country.country" :value="country.country">
            {{ country.country }} ({{ country.total_tasks }})
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>状态:</label>
        <select v-model="selectedEnabled" @change="filterTasks">
          <option value="">全部</option>
          <option value="true">已启用</option>
          <option value="false">已禁用</option>
        </select>
      </div>

      <div class="filter-group">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索新闻源名称..."
          class="search-input"
        />
      </div>
    </div>

    <!-- 任务表格 -->
    <div class="table-container">
      <table class="task-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>新闻源</th>
            <th>国家/地区</th>
            <th>URL</th>
            <th>状态</th>
            <th>间隔(分钟)</th>
            <th>最后爬取</th>
            <th>下次爬取</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in filteredTasks" :key="task.id">
            <td>{{ task.id }}</td>
            <td class="task-name">
              <strong>{{ task.source_name }}</strong>
              <small>{{ task.source_id }}</small>
            </td>
            <td>{{ task.country }}</td>
            <td class="task-url">
              <a :href="task.url" target="_blank" rel="noopener">
                {{ truncateUrl(task.url) }}
              </a>
            </td>
            <td>
              <span :class="['status-badge', task.enabled ? 'enabled' : 'disabled']">
                {{ task.enabled ? '已启用' : '已禁用' }}
              </span>
            </td>
            <td>
              <input 
                type="number" 
                :value="task.interval_minutes" 
                @change="updateInterval(task, $event)"
                class="interval-input"
                min="1"
              />
            </td>
            <td>{{ formatTime(task.last_crawl_time) }}</td>
            <td>{{ formatTime(task.next_crawl_time) }}</td>
            <td class="actions">
              <button 
                @click="toggleEnabled(task)" 
                :class="['btn-sm', task.enabled ? 'btn-warning' : 'btn-success']"
              >
                {{ task.enabled ? '禁用' : '启用' }}
              </button>
              <button @click="runTask(task)" class="btn-sm btn-primary">
                执行
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <span>共 {{ filteredTasks.length }} 个任务</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Task, CountryStats } from '@/types/scheduler';

const props = defineProps<{
  tasks: Task[];
  countries: CountryStats[];
}>();

const emit = defineEmits<{
  update: [sourceId: string, data: { enabled?: boolean; interval_minutes?: number }];
  run: [sourceId: string];
}>();

const selectedCountry = ref('');
const selectedEnabled = ref('');
const searchQuery = ref('');

// 过滤任务
const filteredTasks = computed(() => {
  let result = props.tasks;

  // 按国家筛选
  if (selectedCountry.value) {
    result = result.filter(t => t.country === selectedCountry.value);
  }

  // 按状态筛选
  if (selectedEnabled.value !== '') {
    const enabled = selectedEnabled.value === 'true';
    result = result.filter(t => t.enabled === enabled);
  }

  // 搜索
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(t => 
      t.source_name.toLowerCase().includes(query) ||
      t.source_id.toLowerCase().includes(query)
    );
  }

  return result;
});

// 切换启用状态
function toggleEnabled(task: Task) {
  emit('update', task.source_id, { enabled: !task.enabled });
}

// 更新间隔
function updateInterval(task: Task, event: Event) {
  const target = event.target as HTMLInputElement;
  const interval = parseInt(target.value);
  if (interval > 0) {
    emit('update', task.source_id, { interval_minutes: interval });
  }
}

// 执行任务
function runTask(task: Task) {
  if (confirm(`确定要执行任务 "${task.source_name}" 吗？`)) {
    emit('run', task.source_id);
  }
}

// 筛选任务
function filterTasks() {
  // 筛选逻辑已在 computed 中处理
}

// 格式化时间
function formatTime(time: string | null): string {
  if (!time) return '-';
  const date = new Date(time);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// 截断URL
function truncateUrl(url: string): string {
  if (url.length > 50) {
    return url.substring(0, 47) + '...';
  }
  return url;
}
</script>

<style scoped>
.task-list {
  width: 100%;
}

/* 筛选器 */
.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-weight: 500;
  color: #333;
}

.filter-group select,
.search-input {
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
}

.search-input {
  min-width: 250px;
}

/* 表格 */
.table-container {
  overflow-x: auto;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.task-table thead {
  background: #fafafa;
}

.task-table th,
.task-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e8e8e8;
}

.task-table th {
  font-weight: 600;
  color: #333;
}

.task-table tbody tr:hover {
  background: #f5f5f5;
}

.task-name {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.task-name strong {
  color: #1890ff;
}

.task-name small {
  color: #999;
  font-size: 12px;
}

.task-url a {
  color: #1890ff;
  text-decoration: none;
}

.task-url a:hover {
  text-decoration: underline;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.enabled {
  background: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.status-badge.disabled {
  background: #fff1f0;
  color: #ff4d4f;
  border: 1px solid #ffccc7;
}

.interval-input {
  width: 70px;
  padding: 4px 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  text-align: center;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-sm {
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-sm.btn-success {
  background: #52c41a;
  color: white;
}

.btn-sm.btn-success:hover {
  background: #45a817;
}

.btn-sm.btn-warning {
  background: #faad14;
  color: white;
}

.btn-sm.btn-warning:hover {
  background: #d98e11;
}

.btn-sm.btn-primary {
  background: #1890ff;
  color: white;
}

.btn-sm.btn-primary:hover {
  background: #1570d9;
}

/* 分页 */
.pagination {
  margin-top: 15px;
  text-align: center;
  color: #666;
  font-size: 14px;
}
</style>
