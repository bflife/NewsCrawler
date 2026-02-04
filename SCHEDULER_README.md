# NewsCrawler 调度系统文档

## 概述

NewsCrawler调度系统提供了一个完整的自动化新闻爬取解决方案，支持定时任务、任务管理、历史追踪等功能。

## 主要功能

### 1. 定时调度
- 支持自定义爬取间隔
- 自动执行爬取任务
- 智能错误重试

### 2. 任务管理
- 启用/禁用任务
- 修改爬取间隔
- 手动触发任务

### 3. 数据持久化
- SQLite数据库存储
- 爬取历史记录
- 文章去重

### 4. 统计分析
- 成功率统计
- 国家/地区分组
- 性能监控

## 使用指南

### 命令行接口

```bash
# 初始化任务
python scheduler_cli.py init --interval 60

# 启动调度器
python scheduler_cli.py start

# 查看任务列表
python scheduler_cli.py list

# 查看历史记录
python scheduler_cli.py history --limit 20

# 手动运行任务
python scheduler_cli.py run zaobao
```

### API接口

```python
# GET /api/scheduler/status
# 获取调度器状态

# POST /api/scheduler/start
# 启动调度器

# GET /api/tasks
# 获取任务列表

# PATCH /api/tasks/{source_id}
# 更新任务配置

# POST /api/tasks/{source_id}/run
# 手动执行任务
```

## 配置说明

### 数据库结构

- `crawl_tasks`: 任务配置表
- `crawl_history`: 爬取历史表
- `crawl_articles`: 文章数据表

### 任务配置

```python
{
    "source_id": "cnn",
    "enabled": true,
    "interval_minutes": 60,
    "url": "https://www.cnn.com"
}
```

## 最佳实践

1. 合理设置爬取间隔（建议>=30分钟）
2. 定期检查失败任务
3. 监控爬取成功率
4. 及时更新选择器配置

## 技术支持

详细文档: [ENHANCED_CRAWLER_REPORT.md](./ENHANCED_CRAWLER_REPORT.md)
