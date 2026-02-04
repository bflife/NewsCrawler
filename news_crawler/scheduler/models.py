"""
数据库模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CrawlTask(BaseModel):
    """爬取任务模型"""
    id: Optional[int] = None
    source_id: str = Field(..., description="新闻源ID")
    source_name: str = Field(..., description="新闻源名称")
    url: str = Field(..., description="新闻源URL")
    country: str = Field(..., description="国家/地区")
    enabled: bool = Field(default=True, description="是否启用")
    interval_minutes: int = Field(default=60, description="爬取间隔（分钟）")
    last_crawl_time: Optional[datetime] = Field(None, description="最后爬取时间")
    next_crawl_time: Optional[datetime] = Field(None, description="下次爬取时间")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CrawlHistory(BaseModel):
    """爬取历史记录"""
    id: Optional[int] = None
    task_id: int = Field(..., description="任务ID")
    source_id: str = Field(..., description="新闻源ID")
    url: str = Field(..., description="新闻源URL")
    status: str = Field(..., description="爬取状态: success, failed")
    articles_count: int = Field(default=0, description="爬取到的文章数")
    error_message: Optional[str] = Field(None, description="错误信息")
    crawl_time: datetime = Field(default_factory=datetime.now)
    duration_seconds: float = Field(default=0, description="爬取耗时（秒）")


class CrawlArticle(BaseModel):
    """爬取的文章"""
    id: Optional[int] = None
    source_id: str = Field(..., description="新闻源ID")
    article_id: str = Field(..., description="文章唯一ID")
    title: str = Field(..., description="文章标题")
    url: str = Field(..., description="文章URL")
    author: Optional[str] = Field(None, description="作者")
    publish_time: Optional[datetime] = Field(None, description="发布时间")
    content: str = Field(..., description="文章内容")
    summary: Optional[str] = Field(None, description="文章摘要")
    category: Optional[str] = Field(None, description="文章分类")
    tags: List[str] = Field(default_factory=list, description="标签")
    images: List[str] = Field(default_factory=list, description="图片URL列表")
    videos: List[str] = Field(default_factory=list, description="视频URL列表")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
