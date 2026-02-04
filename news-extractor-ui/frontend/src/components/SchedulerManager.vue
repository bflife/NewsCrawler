<template>
  <div class="scheduler-manager">
    <!-- 头部统计 -->
    <div class="stats-header">
      <div class="stats-card">
        <div class="stat-value">{{ stats.total_tasks }}</div>
        <div class="stat-label">总任务数</div>
      </div>
      <div class="stats-card">
        <div class="stat-value">{{ stats.enabled_tasks }}</div>
        <div class="stat-label">已启用</div>
      </div>
      <div class="stats-card">
        <div class="stat-value">{{ stats.countries }}</div>
        <div class="stat-label">国家/地区</div>
      </div>
      <div class="stats-card">
        <div class="stat-value">{{ stats.recent_success }}</div>
        <div class="stat-label">最近成功</div>
      </div>
      <div class="stats-card">
        <div class="stat-value">{{ stats.recent_failed }}</div>
        <div class="stat-label">最近失败</div>
      </div>
    </div>

    <!-- 调度器控制 -->
    <div class="scheduler-control">
      <div class="control-status">
        <span class="status-indicator" :class="{ active: schedulerStatus.running }"></span>
        <span class="status-text">
          调度器状态: {{ schedulerStatus.running ? '运行中' : '已停止' }}
        </span>
        <span class="crawler-count">
          (已注册 {{ schedulerStatus.registered_crawlers }} 个爬虫)
        </span>
      </div>
      <div class="control-buttons">
        <button 
          @click="startScheduler" 
          :disabled="schedulerStatus.running || loading"
          class="btn btn-success"
        >
          <span v-if="!loading">启动调度器</span>
          <span v-else>处理中...</span>
        </button>
        <button 
          @click="stopScheduler" 
          :disabled="!schedulerStatus.running || loading"
          class="btn btn-danger"
        >
          <span v-if="!loading">停止调度器</span>
          <span v-else>处理中...</span>
        </button>
        <button @click="initTasks" :disabled="loading" class="btn btn-primary">
          初始化任务
        </button>
        <button @click="refreshData" :disabled="loading" class="btn btn-secondary">
          刷新数据
        </button>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        @click="activeTab = tab.value"
        :class="['tab-button', { active: activeTab === tab.value }]"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 任务列表标签 -->
    <div v-if="activeTab === 'tasks'" class="tab-content">
      <TaskList 
        :tasks="tasks" 
        :countries="countries"
        @update="handleTaskUpdate"
        @run="handleTaskRun"
      />
    </div>

    <!-- 历史记录标签 -->
    <div v-if="activeTab === 'history'" class="tab-content">
      <HistoryList :history="history" />
    </div>

    <!-- 国家统计标签 -->
    <div v-if="activeTab === 'countries'" class="tab-content">
      <CountryStats :countries-list="stats.countries_list" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { schedulerApi } from '@/services/schedulerApi';
import type { Task, History, Stats, SchedulerStatus, CountryStats } from '@/types/scheduler';
import TaskList from './TaskList.vue';
import HistoryList from './HistoryList.vue';
import CountryStats from './CountryStats.vue';

const activeTab = ref('tasks');
const loading = ref(false);

const tabs = [
  { label: '任务列表', value: 'tasks' },
  { label: '历史记录', value: 'history' },
  { label: '国家统计', value: 'countries' },
];

const schedulerStatus = ref<SchedulerStatus>({
  running: false,
  registered_crawlers: 0
});

const stats = ref<Stats>({
  total_tasks: 0,
  enabled_tasks: 0,
  disabled_tasks: 0,
  recent_success: 0,
  recent_failed: 0,
  countries: 0,
  countries_list: []
});

const tasks = ref<Task[]>([]);
const history = ref<History[]>([]);
const countries = ref<CountryStats[]>([]);

// 加载数据
async function loadData() {
  try {
    loading.value = true;
    
    // 并行加载所有数据
    const [statusData, statsData, tasksData, historyData, countriesData] = await Promise.all([
      schedulerApi.getStatus(),
      schedulerApi.getStats(),
      schedulerApi.getTasks(),
      schedulerApi.getHistory({ limit: 50 }),
      schedulerApi.getCountries()
    ]);

    schedulerStatus.value = statusData;
    stats.value = statsData;
    tasks.value = tasksData;
    history.value = historyData;
    countries.value = countriesData.countries;
  } catch (error) {
    console.error('加载数据失败:', error);
    alert('加载数据失败，请检查后端服务是否运行');
  } finally {
    loading.value = false;
  }
}

// 启动调度器
async function startScheduler() {
  try {
    loading.value = true;
    const result = await schedulerApi.start();
    alert(result.message);
    await loadData();
  } catch (error: any) {
    alert('启动失败: ' + (error.response?.data?.detail || error.message));
  } finally {
    loading.value = false;
  }
}

// 停止调度器
async function stopScheduler() {
  try {
    loading.value = true;
    const result = await schedulerApi.stop();
    alert(result.message);
    await loadData();
  } catch (error: any) {
    alert('停止失败: ' + (error.response?.data?.detail || error.message));
  } finally {
    loading.value = false;
  }
}

// 初始化任务
async function initTasks() {
  const interval = prompt('请输入爬取间隔（分钟）:', '60');
  if (!interval) return;
  
  const intervalMinutes = parseInt(interval);
  if (isNaN(intervalMinutes) || intervalMinutes < 1) {
    alert('请输入有效的间隔时间');
    return;
  }

  try {
    loading.value = true;
    const result = await schedulerApi.initTasks(intervalMinutes);
    alert(`${result.message}\n总任务数: ${result.total_tasks}`);
    await loadData();
  } catch (error: any) {
    alert('初始化失败: ' + (error.response?.data?.detail || error.message));
  } finally {
    loading.value = false;
  }
}

// 刷新数据
async function refreshData() {
  await loadData();
}

// 处理任务更新
async function handleTaskUpdate(sourceId: string, data: { enabled?: boolean; interval_minutes?: number }) {
  try {
    await schedulerApi.updateTask(sourceId, data);
    await loadData();
  } catch (error: any) {
    alert('更新失败: ' + (error.response?.data?.detail || error.message));
  }
}

// 处理任务执行
async function handleTaskRun(sourceId: string) {
  try {
    const result = await schedulerApi.runTask(sourceId);
    alert(result.message);
    // 等待几秒后刷新数据
    setTimeout(() => loadData(), 3000);
  } catch (error: any) {
    alert('执行失败: ' + (error.response?.data?.detail || error.message));
  }
}

onMounted(() => {
  loadData();
  // 每30秒自动刷新一次
  setInterval(loadData, 30000);
});
</script>

<style scoped>
.scheduler-manager {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 统计卡片 */
.stats-header {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.stats-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

/* 调度器控制 */
.scheduler-control {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.control-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ccc;
  animation: pulse 2s infinite;
}

.status-indicator.active {
  background: #52c41a;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-weight: bold;
  font-size: 16px;
}

.crawler-count {
  color: #666;
  font-size: 14px;
}

.control-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* 按钮 */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-success {
  background: #52c41a;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #45a817;
}

.btn-danger {
  background: #ff4d4f;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #d93638;
}

.btn-primary {
  background: #1890ff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #1570d9;
}

.btn-secondary {
  background: #d9d9d9;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background: #bfbfbf;
}

/* 标签页 */
.tabs {
  display: flex;
  gap: 2px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e8e8e8;
}

.tab-button {
  padding: 12px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  color: #666;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
}

.tab-button:hover {
  color: #1890ff;
}

.tab-button.active {
  color: #1890ff;
  border-bottom-color: #1890ff;
}

.tab-content {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
