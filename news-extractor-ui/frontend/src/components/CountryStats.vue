<template>
  <div class="country-stats">
    <h3>国家/地区统计</h3>
    
    <div class="stats-grid">
      <div v-for="country in sortedCountries" :key="country.country" class="country-card">
        <div class="country-header">
          <h4>{{ country.country }}</h4>
          <span class="total-badge">{{ country.total_tasks }} 个任务</span>
        </div>
        
        <div class="country-stats-detail">
          <div class="stat-item">
            <div class="stat-circle enabled">
              <span>{{ country.enabled_tasks }}</span>
            </div>
            <div class="stat-label">已启用</div>
          </div>
          
          <div class="stat-item">
            <div class="stat-circle disabled">
              <span>{{ country.disabled_tasks }}</span>
            </div>
            <div class="stat-label">已禁用</div>
          </div>
        </div>

        <div class="country-progress">
          <div 
            class="progress-bar"
            :style="{ width: getEnabledPercentage(country) + '%' }"
          ></div>
        </div>
        <div class="progress-label">
          {{ getEnabledPercentage(country).toFixed(1) }}% 已启用
        </div>
      </div>
    </div>

    <div v-if="countriesList.length === 0" class="empty-state">
      暂无数据
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { CountryStats } from '@/types/scheduler';

const props = defineProps<{
  countriesList: CountryStats[];
}>();

// 按任务数量排序
const sortedCountries = computed(() => {
  return [...props.countriesList].sort((a, b) => b.total_tasks - a.total_tasks);
});

function getEnabledPercentage(country: CountryStats): number {
  if (country.total_tasks === 0) return 0;
  return (country.enabled_tasks / country.total_tasks) * 100;
}
</script>

<style scoped>
.country-stats h3 {
  margin-bottom: 20px;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.country-card {
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s;
}

.country-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.country-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.country-header h4 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.total-badge {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.country-stats-detail {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
  font-size: 20px;
  font-weight: bold;
}

.stat-circle.enabled {
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
}

.stat-circle.disabled {
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  color: white;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.country-progress {
  width: 100%;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #52c41a 0%, #73d13d 100%);
  transition: width 0.3s;
}

.progress-label {
  text-align: center;
  font-size: 12px;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}
</style>
