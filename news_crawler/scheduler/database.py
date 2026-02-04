"""
SQLite 数据库管理
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from contextlib import contextmanager

from .models import CrawlTask, CrawlHistory, CrawlArticle


class DatabaseManager:
    """数据库管理器"""

    def __init__(self, db_path: str = "data/news_crawler.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 爬取任务表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT UNIQUE NOT NULL,
                    source_name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    country TEXT NOT NULL,
                    enabled INTEGER DEFAULT 1,
                    interval_minutes INTEGER DEFAULT 60,
                    last_crawl_time TEXT,
                    next_crawl_time TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')

            # 爬取历史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    source_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    articles_count INTEGER DEFAULT 0,
                    error_message TEXT,
                    crawl_time TEXT NOT NULL,
                    duration_seconds REAL DEFAULT 0,
                    FOREIGN KEY (task_id) REFERENCES crawl_tasks(id)
                )
            ''')

            # 文章表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    article_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    author TEXT,
                    publish_time TEXT,
                    content TEXT NOT NULL,
                    summary TEXT,
                    category TEXT,
                    tags TEXT,
                    images TEXT,
                    videos TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(source_id, article_id)
                )
            ''')

            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_source_id 
                ON crawl_tasks(source_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_enabled 
                ON crawl_tasks(enabled)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_history_task_id 
                ON crawl_history(task_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_articles_source_id 
                ON crawl_articles(source_id)
            ''')

            conn.commit()

    # ===== CrawlTask CRUD =====

    def create_task(self, task: CrawlTask) -> int:
        """创建爬取任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO crawl_tasks 
                (source_id, source_name, url, country, enabled, interval_minutes, 
                 last_crawl_time, next_crawl_time, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.source_id,
                task.source_name,
                task.url,
                task.country,
                int(task.enabled),
                task.interval_minutes,
                task.last_crawl_time.isoformat() if task.last_crawl_time else None,
                task.next_crawl_time.isoformat() if task.next_crawl_time else None,
                task.created_at.isoformat(),
                task.updated_at.isoformat()
            ))
            return cursor.lastrowid

    def get_task_by_source_id(self, source_id: str) -> Optional[CrawlTask]:
        """根据source_id获取任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM crawl_tasks WHERE source_id = ?', (source_id,))
            row = cursor.fetchone()
            return self._row_to_task(row) if row else None

    def get_all_tasks(self, enabled_only: bool = False) -> List[CrawlTask]:
        """获取所有任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if enabled_only:
                cursor.execute('SELECT * FROM crawl_tasks WHERE enabled = 1')
            else:
                cursor.execute('SELECT * FROM crawl_tasks')
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def get_tasks_by_country(self, country: str) -> List[CrawlTask]:
        """根据国家获取任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM crawl_tasks WHERE country = ?', (country,))
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def update_task(self, task: CrawlTask):
        """更新任务"""
        task.updated_at = datetime.now()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE crawl_tasks 
                SET source_name = ?, url = ?, country = ?, enabled = ?, 
                    interval_minutes = ?, last_crawl_time = ?, next_crawl_time = ?, 
                    updated_at = ?
                WHERE source_id = ?
            ''', (
                task.source_name,
                task.url,
                task.country,
                int(task.enabled),
                task.interval_minutes,
                task.last_crawl_time.isoformat() if task.last_crawl_time else None,
                task.next_crawl_time.isoformat() if task.next_crawl_time else None,
                task.updated_at.isoformat(),
                task.source_id
            ))

    def delete_task(self, source_id: str):
        """删除任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM crawl_tasks WHERE source_id = ?', (source_id,))

    # ===== CrawlHistory CRUD =====

    def create_history(self, history: CrawlHistory) -> int:
        """创建爬取历史"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO crawl_history 
                (task_id, source_id, url, status, articles_count, 
                 error_message, crawl_time, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                history.task_id,
                history.source_id,
                history.url,
                history.status,
                history.articles_count,
                history.error_message,
                history.crawl_time.isoformat(),
                history.duration_seconds
            ))
            return cursor.lastrowid

    def get_history_by_task_id(self, task_id: int, limit: int = 100) -> List[CrawlHistory]:
        """根据任务ID获取历史记录"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM crawl_history 
                WHERE task_id = ? 
                ORDER BY crawl_time DESC 
                LIMIT ?
            ''', (task_id, limit))
            return [self._row_to_history(row) for row in cursor.fetchall()]

    def get_recent_history(self, limit: int = 100) -> List[CrawlHistory]:
        """获取最近的爬取历史"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM crawl_history 
                ORDER BY crawl_time DESC 
                LIMIT ?
            ''', (limit,))
            return [self._row_to_history(row) for row in cursor.fetchall()]

    # ===== CrawlArticle CRUD =====

    def create_article(self, article: CrawlArticle) -> Optional[int]:
        """创建文章（如果已存在则跳过）"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO crawl_articles 
                    (source_id, article_id, title, url, author, publish_time, 
                     content, summary, category, tags, images, videos, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article.source_id,
                    article.article_id,
                    article.title,
                    article.url,
                    article.author,
                    article.publish_time.isoformat() if article.publish_time else None,
                    article.content,
                    article.summary,
                    article.category,
                    json.dumps(article.tags),
                    json.dumps(article.images),
                    json.dumps(article.videos),
                    article.created_at.isoformat(),
                    article.updated_at.isoformat()
                ))
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # 文章已存在
            return None

    def get_articles_by_source(self, source_id: str, limit: int = 100) -> List[CrawlArticle]:
        """根据新闻源获取文章"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM crawl_articles 
                WHERE source_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (source_id, limit))
            return [self._row_to_article(row) for row in cursor.fetchall()]

    def article_exists(self, source_id: str, article_id: str) -> bool:
        """检查文章是否已存在"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM crawl_articles 
                WHERE source_id = ? AND article_id = ?
            ''', (source_id, article_id))
            return cursor.fetchone()[0] > 0

    # ===== Helper Methods =====

    def _row_to_task(self, row: sqlite3.Row) -> CrawlTask:
        """将数据库行转换为CrawlTask"""
        return CrawlTask(
            id=row['id'],
            source_id=row['source_id'],
            source_name=row['source_name'],
            url=row['url'],
            country=row['country'],
            enabled=bool(row['enabled']),
            interval_minutes=row['interval_minutes'],
            last_crawl_time=datetime.fromisoformat(row['last_crawl_time']) if row['last_crawl_time'] else None,
            next_crawl_time=datetime.fromisoformat(row['next_crawl_time']) if row['next_crawl_time'] else None,
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )

    def _row_to_history(self, row: sqlite3.Row) -> CrawlHistory:
        """将数据库行转换为CrawlHistory"""
        return CrawlHistory(
            id=row['id'],
            task_id=row['task_id'],
            source_id=row['source_id'],
            url=row['url'],
            status=row['status'],
            articles_count=row['articles_count'],
            error_message=row['error_message'],
            crawl_time=datetime.fromisoformat(row['crawl_time']),
            duration_seconds=row['duration_seconds']
        )

    def _row_to_article(self, row: sqlite3.Row) -> CrawlArticle:
        """将数据库行转换为CrawlArticle"""
        return CrawlArticle(
            id=row['id'],
            source_id=row['source_id'],
            article_id=row['article_id'],
            title=row['title'],
            url=row['url'],
            author=row['author'],
            publish_time=datetime.fromisoformat(row['publish_time']) if row['publish_time'] else None,
            content=row['content'],
            summary=row['summary'],
            category=row['category'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            images=json.loads(row['images']) if row['images'] else [],
            videos=json.loads(row['videos']) if row['videos'] else [],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )
