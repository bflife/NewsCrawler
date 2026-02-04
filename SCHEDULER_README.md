# 新闻爬虫调度系统

## 概述

本系统扩展了原有的NewsCrawler项目，增加了以下核心功能：

1. **国家/地区分类系统** - 支持按国家和地区分类管理新闻源
2. **定时调度系统** - 支持用户自定义时间间隔的定时爬取
3. **通用爬虫框架** - 提供可扩展的通用爬虫基类
4. **数据库管理** - SQLite数据库存储爬取历史和任务配置
5. **多新闻源支持** - 已集成200+全球新闻网站

## 支持的国家/地区

目前支持以下国家和地区的新闻源：

- 🇨🇳 **中国大陆** - 国内主流新闻网站
- 🇭🇰 **香港** - 大公报、苹果日报、香港01等20+网站
- 🇹🇼 **台湾** - 自由时报、联合报、中时电子报等17+网站
- 🇸🇬 **新加坡** - 联合早报
- 🇲🇾 **马来西亚** - 星洲日报、南洋商报等10+网站
- 🇯🇵 **日本** - NHK、朝日新闻、读卖新闻等18+网站
- 🇰🇷 **韩国** - 韩联社、朝鲜日报等
- 🇺🇸 **美国** - CNN、纽约时报、华尔街日报等40+网站
- 🇬🇧 **英国** - BBC、路透社、金融时报等8+网站
- 🇫🇷 **法国** - 法新社、世界报等5+网站
- 🇷🇺 **俄罗斯** - 俄罗斯卫星通讯社等4+网站
- 🇦🇺 **澳大利亚** - 澳大利亚广播公司、每日电讯报等
- 🇲🇴 **澳门** - 澳门日报、力报等10+网站
- 🇻🇳 **越南** - 越南通讯社等
- 🇮🇳 **印度** - 印度斯坦时报等
- 以及其他国家和地区...

## 项目结构

```
news_crawler/
├── config/
│   └── news_sources.json      # 新闻源配置文件（200+网站）
├── scheduler/
│   ├── __init__.py
│   ├── models.py               # 数据模型（任务、历史、文章）
│   ├── database.py             # SQLite数据库管理
│   └── scheduler.py            # 调度器核心
├── generic/
│   ├── __init__.py
│   └── crawler.py              # 通用爬虫基类
├── sites/
│   ├── __init__.py
│   └── crawlers.py             # 具体网站爬虫实现
└── ...

scheduler_cli.py                # 命令行管理工具
data/
└── news_crawler.db             # SQLite数据库文件
```

## 快速开始

### 1. 安装依赖

```bash
# 确保已安装uv
uv sync
```

### 2. 初始化任务

从配置文件加载所有新闻源并创建爬取任务：

```bash
# 初始化任务，默认60分钟间隔
uv run python scheduler_cli.py init --interval 60

# 或指定其他间隔（例如120分钟）
uv run python scheduler_cli.py init --interval 120
```

### 3. 查看任务

```bash
# 列出所有任务
uv run python scheduler_cli.py list

# 列出指定国家的任务
uv run python scheduler_cli.py list --country 台湾
uv run python scheduler_cli.py list --country 香港
uv run python scheduler_cli.py list --country 日本

# 列出所有国家
uv run python scheduler_cli.py countries
```

### 4. 启动调度器

```bash
# 启动后台调度器（每分钟检查一次任务）
uv run python scheduler_cli.py start
```

调度器会：
- 每60秒检查一次所有任务
- 对于到期的任务，自动执行爬取
- 将爬取结果保存到数据库
- 记录爬取历史和错误信息

### 5. 手动执行任务

```bash
# 执行指定新闻源的爬取任务
uv run python scheduler_cli.py run --source-id zaobao

# 执行所有到期的任务
uv run python scheduler_cli.py run
```

### 6. 查看爬取历史

```bash
# 查看最近20条爬取历史
uv run python scheduler_cli.py history --limit 20

# 查看指定新闻源的历史
uv run python scheduler_cli.py history --source-id zaobao --limit 50
```

### 7. 管理任务

```bash
# 查看统计信息
uv run python scheduler_cli.py stats

# 启用/禁用任务
uv run python scheduler_cli.py enable --source-id zaobao
uv run python scheduler_cli.py disable --source-id zaobao

# 设置任务间隔（分钟）
uv run python scheduler_cli.py set-interval --source-id zaobao --interval 120
```

## 命令行工具详解

### init - 初始化任务

从配置文件加载新闻源并创建爬取任务。

```bash
uv run python scheduler_cli.py init [--interval MINUTES]
```

参数：
- `--interval`: 默认爬取间隔（分钟），默认60

### start - 启动调度器

启动后台调度器，自动执行定时任务。

```bash
uv run python scheduler_cli.py start
```

按 `Ctrl+C` 停止调度器。

### run - 手动执行任务

手动触发爬取任务。

```bash
uv run python scheduler_cli.py run [--source-id SOURCE_ID]
```

参数：
- `--source-id`: 指定新闻源ID，不指定则执行所有到期任务

### list - 列出任务

列出所有或指定国家的爬取任务。

```bash
uv run python scheduler_cli.py list [--country COUNTRY]
```

参数：
- `--country`: 按国家/地区筛选，例如："台湾"、"香港"、"日本"

### countries - 列出所有国家

列出所有已配置的国家/地区及其任务数量。

```bash
uv run python scheduler_cli.py countries
```

### history - 查看爬取历史

查看爬取历史记录，包括成功/失败状态、文章数、耗时等。

```bash
uv run python scheduler_cli.py history [--source-id SOURCE_ID] [--limit N]
```

参数：
- `--source-id`: 指定新闻源ID
- `--limit`: 显示数量，默认20

### stats - 统计信息

查看调度器的统计信息。

```bash
uv run python scheduler_cli.py stats
```

输出信息：
- 总任务数
- 启用/禁用任务数
- 国家/地区数
- 最近成功/失败次数

### enable/disable - 启用/禁用任务

启用或禁用指定的爬取任务。

```bash
uv run python scheduler_cli.py enable --source-id SOURCE_ID
uv run python scheduler_cli.py disable --source-id SOURCE_ID
```

### set-interval - 设置任务间隔

设置指定任务的爬取间隔时间。

```bash
uv run python scheduler_cli.py set-interval --source-id SOURCE_ID --interval MINUTES
```

## 数据库结构

系统使用SQLite数据库（`data/news_crawler.db`）存储以下信息：

### crawl_tasks 表
爬取任务配置

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| source_id | TEXT | 新闻源ID（唯一） |
| source_name | TEXT | 新闻源名称 |
| url | TEXT | 新闻源URL |
| country | TEXT | 国家/地区 |
| enabled | INTEGER | 是否启用（0/1） |
| interval_minutes | INTEGER | 爬取间隔（分钟） |
| last_crawl_time | TEXT | 最后爬取时间 |
| next_crawl_time | TEXT | 下次爬取时间 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### crawl_history 表
爬取历史记录

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| task_id | INTEGER | 任务ID（外键） |
| source_id | TEXT | 新闻源ID |
| url | TEXT | 新闻源URL |
| status | TEXT | 状态（success/failed） |
| articles_count | INTEGER | 爬取文章数 |
| error_message | TEXT | 错误信息 |
| crawl_time | TEXT | 爬取时间 |
| duration_seconds | REAL | 耗时（秒） |

### crawl_articles 表
爬取的文章

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| source_id | TEXT | 新闻源ID |
| article_id | TEXT | 文章唯一ID |
| title | TEXT | 标题 |
| url | TEXT | 文章URL |
| author | TEXT | 作者 |
| publish_time | TEXT | 发布时间 |
| content | TEXT | 内容 |
| summary | TEXT | 摘要 |
| category | TEXT | 分类 |
| tags | TEXT | 标签（JSON） |
| images | TEXT | 图片列表（JSON） |
| videos | TEXT | 视频列表（JSON） |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

## 扩展新的新闻源

### 方法1：使用SimpleListCrawler（推荐）

对于标准的"列表页 + 详情页"结构的新闻网站，可以直接使用`SimpleListCrawler`：

```python
from news_crawler.generic.crawler import SimpleListCrawler

def create_my_news_crawler():
    return SimpleListCrawler(
        source_id="my_news",
        source_name="我的新闻网",
        base_url="https://www.mynews.com",
        list_url="https://www.mynews.com/news",
        list_selector="div.news-item",           # 文章列表项选择器
        title_selector="h3.title::text",         # 标题选择器
        link_selector="a::attr(href)",           # 链接选择器
        article_title_selector="h1.headline::text",     # 文章页标题
        article_content_selector="div.content p",        # 文章页内容
        article_time_selector="time::text",              # 发布时间
        article_author_selector="span.author::text"      # 作者
    )
```

### 方法2：继承GenericNewsCrawler

对于复杂的网站结构，可以继承`GenericNewsCrawler`并实现自定义逻辑：

```python
from news_crawler.generic.crawler import GenericNewsCrawler
from parsel import Selector

class MyNewsCrawler(GenericNewsCrawler):
    def get_article_list_selector(self) -> str:
        return "div.article-list > article"
    
    def parse_article_item(self, element: Selector):
        title = element.css("h2.title::text").get()
        url = element.css("a.link::attr(href)").get()
        return {"title": title, "url": url}
    
    def parse_article_content(self, html: str, url: str):
        # 自定义解析逻辑
        selector = Selector(html)
        # ...
        return news_item
```

### 注册爬虫

在`news_crawler/sites/crawlers.py`中注册新爬虫：

```python
CRAWLER_FACTORIES = {
    # ... 现有爬虫
    'my_news': create_my_news_crawler,
}
```

### 添加到配置文件

在`news_crawler/config/news_sources.json`中添加新闻源：

```json
{
  "id": "my_news",
  "name": "我的新闻网",
  "country": "中国",
  "url": "https://www.mynews.com",
  "category": "综合",
  "language": "zh-CN",
  "enabled": true
}
```

## 使用示例

### 示例1：按国家爬取新闻

```bash
# 1. 列出台湾的所有新闻源
uv run python scheduler_cli.py list --country 台湾

# 2. 手动执行台湾某个新闻源
uv run python scheduler_cli.py run --source-id ltn

# 3. 查看爬取结果
uv run python scheduler_cli.py history --source-id ltn
```

### 示例2：设置不同间隔

```bash
# 重要新闻源设置较短间隔（30分钟）
uv run python scheduler_cli.py set-interval --source-id cnn --interval 30
uv run python scheduler_cli.py set-interval --source-id bbc --interval 30

# 一般新闻源设置正常间隔（60分钟）
uv run python scheduler_cli.py set-interval --source-id zaobao --interval 60

# 不太重要的源设置较长间隔（180分钟）
uv run python scheduler_cli.py set-interval --source-id some_news --interval 180
```

### 示例3：监控爬取状态

```bash
# 启动调度器
uv run python scheduler_cli.py start

# 在另一个终端监控
watch -n 10 "uv run python scheduler_cli.py stats"
watch -n 30 "uv run python scheduler_cli.py history --limit 10"
```

## 注意事项

1. **遵守robots.txt** - 请遵守目标网站的爬虫协议
2. **控制频率** - 建议设置合理的爬取间隔，避免对目标服务器造成压力
3. **异常处理** - 系统会自动记录失败的任务，可通过history命令查看
4. **数据去重** - 系统会自动检测并跳过已爬取的文章（基于source_id + article_id）
5. **仅供学习** - 本项目仅供学习和研究使用，不得用于商业用途

## 技术栈

- **Python 3.8+**
- **SQLite 3** - 数据存储
- **curl_cffi** - HTTP请求
- **parsel** - HTML解析
- **tenacity** - 重试机制
- **threading** - 多线程调度

## 未来计划

- [ ] Web UI管理界面
- [ ] 更多新闻源支持
- [ ] RSS订阅支持
- [ ] 文章去重算法优化
- [ ] 分布式爬取支持
- [ ] 数据导出功能（CSV、Excel）
- [ ] 实时推送通知
- [ ] AI内容摘要

## 许可证

本项目仅供学习和研究使用。使用本项目即表示您同意：
- 不将其用于商业目的
- 不进行大规模爬取
- 遵守相关法律法规和目标网站的使用条款

## 贡献

欢迎提交Issue和Pull Request！

特别欢迎贡献：
- 新的新闻源支持
- 爬虫算法优化
- Bug修复
- 文档改进
