"""
调度器管理 API
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

from news_crawler.scheduler import NewsScheduler
from news_crawler.sites import register_all_crawlers

router = APIRouter()

# 全局调度器实例
_scheduler: Optional[NewsScheduler] = None


def get_scheduler() -> NewsScheduler:
    """获取调度器实例"""
    global _scheduler
    if _scheduler is None:
        _scheduler = NewsScheduler()
        register_all_crawlers(_scheduler)
    return _scheduler


# ===== 响应模型 =====

class TaskResponse(BaseModel):
    """任务响应模型"""
    id: int
    source_id: str
    source_name: str
    url: str
    country: str
    enabled: bool
    interval_minutes: int
    last_crawl_time: Optional[datetime]
    next_crawl_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class HistoryResponse(BaseModel):
    """历史记录响应模型"""
    id: int
    task_id: int
    source_id: str
    url: str
    status: str
    articles_count: int
    error_message: Optional[str]
    crawl_time: datetime
    duration_seconds: float


class ArticleResponse(BaseModel):
    """文章响应模型"""
    id: int
    source_id: str
    article_id: str
    title: str
    url: str
    author: Optional[str]
    publish_time: Optional[datetime]
    summary: Optional[str]
    category: Optional[str]
    created_at: datetime


class CountryStatsResponse(BaseModel):
    """国家统计响应"""
    country: str
    total_tasks: int
    enabled_tasks: int
    disabled_tasks: int


class StatsResponse(BaseModel):
    """统计信息响应"""
    total_tasks: int
    enabled_tasks: int
    disabled_tasks: int
    recent_success: int
    recent_failed: int
    countries: int
    countries_list: List[CountryStatsResponse]


class TaskUpdateRequest(BaseModel):
    """任务更新请求"""
    enabled: Optional[bool] = None
    interval_minutes: Optional[int] = None


# ===== API 路由 =====

@router.get("/scheduler/status")
async def get_scheduler_status():
    """获取调度器状态"""
    scheduler = get_scheduler()
    return {
        "running": scheduler.running,
        "registered_crawlers": len(scheduler.crawlers)
    }


@router.post("/scheduler/start")
async def start_scheduler():
    """启动调度器"""
    scheduler = get_scheduler()
    if scheduler.running:
        raise HTTPException(status_code=400, detail="调度器已经在运行")
    scheduler.start()
    return {"message": "调度器已启动", "running": True}


@router.post("/scheduler/stop")
async def stop_scheduler():
    """停止调度器"""
    scheduler = get_scheduler()
    if not scheduler.running:
        raise HTTPException(status_code=400, detail="调度器未运行")
    scheduler.stop()
    return {"message": "调度器已停止", "running": False}


@router.get("/scheduler/stats", response_model=StatsResponse)
async def get_stats():
    """获取统计信息"""
    scheduler = get_scheduler()
    stats = scheduler.get_task_statistics()
    
    # 获取各国家统计
    countries = scheduler.get_all_countries()
    countries_list = []
    for country in countries:
        tasks = scheduler.get_tasks_by_country(country)
        enabled = sum(1 for t in tasks if t.enabled)
        countries_list.append(CountryStatsResponse(
            country=country,
            total_tasks=len(tasks),
            enabled_tasks=enabled,
            disabled_tasks=len(tasks) - enabled
        ))
    
    return StatsResponse(
        total_tasks=stats['total_tasks'],
        enabled_tasks=stats['enabled_tasks'],
        disabled_tasks=stats['disabled_tasks'],
        recent_success=stats['recent_success'],
        recent_failed=stats['recent_failed'],
        countries=stats['countries'],
        countries_list=countries_list
    )


@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    country: Optional[str] = Query(None, description="按国家筛选"),
    enabled: Optional[bool] = Query(None, description="按启用状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """获取任务列表"""
    scheduler = get_scheduler()
    
    if country:
        tasks = scheduler.get_tasks_by_country(country)
    else:
        tasks = scheduler.db.get_all_tasks()
    
    # 按启用状态筛选
    if enabled is not None:
        tasks = [t for t in tasks if t.enabled == enabled]
    
    # 分页
    total = len(tasks)
    start = (page - 1) * page_size
    end = start + page_size
    tasks = tasks[start:end]
    
    return [TaskResponse(
        id=t.id,
        source_id=t.source_id,
        source_name=t.source_name,
        url=t.url,
        country=t.country,
        enabled=t.enabled,
        interval_minutes=t.interval_minutes,
        last_crawl_time=t.last_crawl_time,
        next_crawl_time=t.next_crawl_time,
        created_at=t.created_at,
        updated_at=t.updated_at
    ) for t in tasks]


@router.get("/tasks/{source_id}", response_model=TaskResponse)
async def get_task(source_id: str):
    """获取单个任务"""
    scheduler = get_scheduler()
    task = scheduler.db.get_task_by_source_id(source_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"任务不存在: {source_id}")
    
    return TaskResponse(
        id=task.id,
        source_id=task.source_id,
        source_name=task.source_name,
        url=task.url,
        country=task.country,
        enabled=task.enabled,
        interval_minutes=task.interval_minutes,
        last_crawl_time=task.last_crawl_time,
        next_crawl_time=task.next_crawl_time,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.patch("/tasks/{source_id}")
async def update_task(source_id: str, update: TaskUpdateRequest):
    """更新任务"""
    scheduler = get_scheduler()
    task = scheduler.db.get_task_by_source_id(source_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"任务不存在: {source_id}")
    
    # 更新字段
    if update.enabled is not None:
        task.enabled = update.enabled
    if update.interval_minutes is not None:
        task.interval_minutes = update.interval_minutes
    
    scheduler.db.update_task(task)
    
    return {"message": "任务已更新", "source_id": source_id}


@router.post("/tasks/{source_id}/run")
async def run_task(source_id: str):
    """手动执行任务"""
    scheduler = get_scheduler()
    task = scheduler.db.get_task_by_source_id(source_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"任务不存在: {source_id}")
    
    # 在后台线程执行（避免阻塞）
    import threading
    def execute():
        scheduler.execute_task(task)
    
    thread = threading.Thread(target=execute, daemon=True)
    thread.start()
    
    return {"message": "任务已开始执行", "source_id": source_id}


@router.get("/countries")
async def get_countries():
    """获取所有国家列表"""
    scheduler = get_scheduler()
    countries = scheduler.get_all_countries()
    
    # 统计每个国家的任务数
    result = []
    for country in countries:
        tasks = scheduler.get_tasks_by_country(country)
        enabled = sum(1 for t in tasks if t.enabled)
        result.append({
            "country": country,
            "total_tasks": len(tasks),
            "enabled_tasks": enabled,
            "disabled_tasks": len(tasks) - enabled
        })
    
    return {"countries": result}


@router.get("/history", response_model=List[HistoryResponse])
async def get_history(
    source_id: Optional[str] = Query(None, description="按新闻源筛选"),
    status: Optional[str] = Query(None, description="按状态筛选: success, failed"),
    limit: int = Query(50, ge=1, le=200, description="返回数量")
):
    """获取爬取历史"""
    scheduler = get_scheduler()
    
    if source_id:
        task = scheduler.db.get_task_by_source_id(source_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"任务不存在: {source_id}")
        history_list = scheduler.db.get_history_by_task_id(task.id, limit=limit)
    else:
        history_list = scheduler.db.get_recent_history(limit=limit)
    
    # 按状态筛选
    if status:
        history_list = [h for h in history_list if h.status == status]
    
    return [HistoryResponse(
        id=h.id,
        task_id=h.task_id,
        source_id=h.source_id,
        url=h.url,
        status=h.status,
        articles_count=h.articles_count,
        error_message=h.error_message,
        crawl_time=h.crawl_time,
        duration_seconds=h.duration_seconds
    ) for h in history_list]


@router.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    source_id: Optional[str] = Query(None, description="按新闻源筛选"),
    limit: int = Query(50, ge=1, le=200, description="返回数量")
):
    """获取爬取的文章"""
    scheduler = get_scheduler()
    
    if source_id:
        articles = scheduler.db.get_articles_by_source(source_id, limit=limit)
    else:
        # 获取所有文章（需要实现这个方法）
        raise HTTPException(status_code=400, detail="请指定source_id")
    
    return [ArticleResponse(
        id=a.id,
        source_id=a.source_id,
        article_id=a.article_id,
        title=a.title,
        url=a.url,
        author=a.author,
        publish_time=a.publish_time,
        summary=a.summary,
        category=a.category,
        created_at=a.created_at
    ) for a in articles]


@router.post("/init")
async def init_tasks(interval_minutes: int = Query(60, description="默认间隔（分钟）")):
    """初始化任务"""
    scheduler = get_scheduler()
    scheduler.init_tasks_from_config(interval_minutes=interval_minutes)
    
    tasks = scheduler.db.get_all_tasks()
    return {
        "message": "任务初始化完成",
        "total_tasks": len(tasks),
        "interval_minutes": interval_minutes
    }
