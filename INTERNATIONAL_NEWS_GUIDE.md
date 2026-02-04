# 国际新闻爬虫快速开始指南

## 📋 概述

本项目新增了国际新闻爬虫功能，支持从全球 130+ 个主流新闻网站自动爬取内容，并提供定时扫描、更新检测和分类管理功能。

## 🌍 支持的网站

### 按地区分类

- **东亚** (19个网站): 日本、韩国、朝鲜
- **东南亚** (15个网站): 马来西亚、新加坡、越南、缅甸
- **大中华** (46个网站): 香港、澳门、台湾
- **欧洲** (19个网站): 英国、法国、德国、爱尔兰、俄罗斯
- **北美** (22个网站): 美国
- **大洋洲** (5个网站): 澳大利亚、新西兰
- **南亚** (3个网站): 印度
- **其他** (3个网站): 阿塞拜疆

### 主要网站

- **美国** (22): 纽约时报、华尔街日报、CNN、BBC、美联社、彭博社等
- **日本** (14): 共同社、NHK、朝日新闻、读卖新闻、日经新闻等
- **香港** (21): 苹果日报、南华早报、香港01、立场新闻等
- **英国** (8): 路透社、金融时报、卫报、泰晤士报等
- **台湾** (13): 自由时报、联合报、中时电子报等

完整列表请查看: `news_crawler/international_news/README.md`

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保已安装基础依赖
pip3 install tenacity parsel requests

# 可选：安装 curl_cffi 以获得更好的爬取效果
pip3 install curl_cffi
```

### 2. 初始化配置

```bash
# 初始化数据库和网站配置
python3 -c "from news_crawler.international_news import ConfigManager; ConfigManager().load_site_configs()"
```

### 3. 基本使用

```bash
# 查看所有支持的国家
python3 -m news_crawler.international_news.cli list --countries

# 查看某个国家的所有网站
python3 -m news_crawler.international_news.cli list --country 美国

# 扫描特定国家的新闻（一次性）
python3 -m news_crawler.international_news.cli scan --country 日本 --max-articles 5

# 扫描整个地区
python3 -m news_crawler.international_news.cli scan --region 东亚 --max-articles 3

# 查看爬取统计
python3 -m news_crawler.international_news.cli stats --days 7
```

### 4. 启动定时扫描

```bash
# 启动持续扫描（每小时检查一次）
python3 -m news_crawler.international_news.cli start --interval 3600

# 只扫描特定国家，每30分钟检查一次
python3 -m news_crawler.international_news.cli start --country 美国 --interval 1800

# 只扫描特定地区
python3 -m news_crawler.international_news.cli start --region 东亚 --interval 3600
```

## 📖 详细使用

### 列出网站

```bash
# 列出所有国家
python3 -m news_crawler.international_news.cli list --countries

# 列出所有地区分组
python3 -m news_crawler.international_news.cli list --regions

# 列出某个国家的网站
python3 -m news_crawler.international_news.cli list --country 日本

# 列出某个地区的所有网站
python3 -m news_crawler.international_news.cli list --region 欧洲
```

### 一次性扫描

```bash
# 扫描所有网站
python3 -m news_crawler.international_news.cli scan --all --max-articles 5

# 扫描特定国家
python3 -m news_crawler.international_news.cli scan --country 美国 --max-articles 10

# 扫描特定地区
python3 -m news_crawler.international_news.cli scan --region 东亚 --max-articles 5

# 显示详细信息和文章列表
python3 -m news_crawler.international_news.cli scan --country 日本 --verbose --show-articles

# 自定义并发线程数
python3 -m news_crawler.international_news.cli scan --all --workers 10 --max-articles 5
```

### 持续定时扫描

```bash
# 默认每小时扫描一次
python3 -m news_crawler.international_news.cli start --interval 3600

# 每30分钟扫描一次特定国家
python3 -m news_crawler.international_news.cli start --country 日本 --interval 1800

# 每2小时扫描一次特定地区
python3 -m news_crawler.international_news.cli start --region 东亚 --interval 7200 --max-articles 10
```

### 查看统计信息

```bash
# 查看最近7天的统计
python3 -m news_crawler.international_news.cli stats --days 7

# 查看统计并显示最近的爬取历史
python3 -m news_crawler.international_news.cli stats --days 30 --history --limit 50
```

### 配置网站

```bash
# 列出所有可配置的网站
python3 -m news_crawler.international_news.cli config --list-sites

# 启用某个网站
python3 -m news_crawler.international_news.cli config --site "BBC" --enable

# 禁用某个网站
python3 -m news_crawler.international_news.cli config --site "CNN" --disable

# 设置扫描间隔（秒）
python3 -m news_crawler.international_news.cli config --site "纽约时报" --interval 7200

# 同时设置多个参数
python3 -m news_crawler.international_news.cli config --site "日经新闻" --enable --interval 3600
```

## 🔧 Python API 使用

### 基本爬取示例

```python
from news_crawler.international_news import InternationalNewsCrawler

# 创建爬虫实例
crawler = InternationalNewsCrawler(
    news_url="https://www.bbc.com/news/world",
    site_config={
        'name': 'BBC',
        'type': 'broadcast',
        'encoding': 'utf-8'
    }
)

# 提取最新文章列表
articles = crawler.extract_latest_articles(max_articles=10)
for article in articles:
    print(f"标题: {article['title']}")
    print(f"URL: {article['url']}\n")

# 爬取单篇文章
crawler_single = InternationalNewsCrawler(
    news_url="https://www.bbc.com/news/world-12345678",
    site_config={'name': 'BBC'}
)
news_item = crawler_single.run()
print(f"标题: {news_item.title}")
print(f"作者: {news_item.meta_info.author_name}")
print(f"内容: {len(news_item.contents)} 个内容项")
```

### 使用配置管理器

```python
from news_crawler.international_news import ConfigManager

# 初始化管理器
manager = ConfigManager()
manager.load_site_configs()

# 获取所有美国网站
us_sites = manager.get_sites_by_filter(country="美国")
print(f"美国有 {len(us_sites)} 个新闻网站")

# 获取需要扫描的网站（根据扫描间隔）
sites_to_scan = manager.get_sites_to_scan()
print(f"当前需要扫描 {len(sites_to_scan)} 个网站")

# 查看统计信息
stats = manager.get_crawl_statistics(days=7)
print(f"7天内爬取次数: {stats['total_crawls']}")
print(f"成功率: {stats['success_rate']}")
print(f"爬取文章总数: {stats['total_articles']}")
```

### 使用调度器进行批量扫描

```python
from news_crawler.international_news import NewsScheduler, ConfigManager

# 初始化
manager = ConfigManager()
manager.load_site_configs()

scheduler = NewsScheduler(
    config_manager=manager,
    max_workers=5  # 并发线程数
)

# 一次性扫描所有网站
results = scheduler.scan_all_sites(max_articles_per_site=10)
print(f"扫描了 {len(results)} 个网站")
print(f"发现 {sum(r['new_articles'] for r in results)} 篇新文章")

# 只扫描特定国家
results = scheduler.scan_all_sites(
    country="日本",
    max_articles_per_site=5,
    parallel=True
)

# 启动持续扫描（阻塞）
scheduler.start_continuous_scanning(
    check_interval=3600,  # 每小时检查一次
    max_articles_per_site=10
)
```

### 自定义回调函数

```python
from news_crawler.international_news import NewsScheduler, ConfigManager

def on_article_crawled(news_item, site_name, country):
    """当文章被爬取时触发"""
    print(f"[{country}] {site_name}: {news_item.title}")
    # 在这里添加自定义处理逻辑
    # 例如：发送通知、存入数据库、触发分析等

manager = ConfigManager()
manager.load_site_configs()

scheduler = NewsScheduler(
    config_manager=manager,
    on_article_crawled=on_article_crawled
)

# 扫描时会触发回调
results = scheduler.scan_all_sites(max_articles_per_site=5)
```

## 📊 数据存储

### 文件存储

爬取的新闻内容保存在 `data/international_news/` 目录下，每篇文章一个 JSON 文件：

```json
{
  "title": "文章标题",
  "news_url": "https://example.com/article",
  "news_id": "unique_id",
  "meta_info": {
    "author_name": "作者名",
    "publish_time": "2024-01-01 12:00:00"
  },
  "contents": [
    {"type": "text", "content": "段落内容", "desc": ""},
    {"type": "image", "content": "图片URL", "desc": "图片描述"}
  ],
  "texts": ["段落1", "段落2"],
  "images": ["图片URL1", "图片URL2"],
  "extra": {
    "site_name": "网站名",
    "site_type": "网站类型",
    "extracted_at": "2024-01-01T12:00:00"
  }
}
```

### 数据库存储

爬取历史存储在 SQLite 数据库 `data/international_news/crawl_history.db`:

- **site_configs**: 网站配置（扫描间隔、启用状态等）
- **crawl_history**: 爬取历史记录
- **latest_articles**: 最新文章追踪（用于更新检测）

## ⚙️ 配置说明

### 扫描间隔

每个网站可以配置独立的扫描间隔（秒）：

- 默认: 3600 秒（1小时）
- 建议范围: 1800-7200 秒（30分钟 - 2小时）
- 重要网站可设置较短间隔
- 不常更新的网站可设置较长间隔

### 并发设置

- `max_workers`: 并发线程数，默认 5
- 建议根据网络带宽调整
- 避免设置过高以免被网站封禁

### 文章数量限制

- `max_articles_per_site`: 每个网站爬取的最大文章数
- 默认: 10 篇
- 建议: 5-20 篇
- 首次运行可设置较大值

## 🎯 使用场景

### 场景1: 监控特定国家的新闻

```bash
# 每30分钟扫描美国主流媒体
python3 -m news_crawler.international_news.cli start \
    --country 美国 \
    --interval 1800 \
    --max-articles 5
```

### 场景2: 监控整个地区的新闻

```bash
# 每小时扫描东亚地区（日本、韩国、朝鲜）
python3 -m news_crawler.international_news.cli start \
    --region 东亚 \
    --interval 3600 \
    --max-articles 10
```

### 场景3: 全球新闻监控

```bash
# 每2小时扫描所有网站
python3 -m news_crawler.international_news.cli start \
    --interval 7200 \
    --max-articles 5 \
    --workers 10
```

### 场景4: 一次性批量采集

```bash
# 一次性采集所有网站的最新内容
python3 -m news_crawler.international_news.cli scan \
    --all \
    --max-articles 20 \
    --workers 10 \
    --verbose
```

## 📝 注意事项

1. **遵守 robots.txt**: 爬取前请检查目标网站的 robots.txt
2. **控制频率**: 避免过于频繁的请求，建议每个网站间隔至少 1-2 秒
3. **网络环境**: 某些网站可能需要代理才能访问
4. **法律合规**: 仅用于学习研究，不得用于商业用途
5. **网站变化**: 网站结构可能变化导致爬取失败，需定期检查

## 🔗 相关文档

- 完整文档: `news_crawler/international_news/README.md`
- 项目主文档: `README.md`
- Docker部署: `DOCKER_DEPLOYMENT.md`

## ❓ 常见问题

### Q: 如何添加新网站？

A: 编辑 `news_crawler/international_news/configs/sites_config.py`，在对应国家列表中添加网站配置。

### Q: 如何修改某个网站的扫描间隔？

A: 使用 config 命令：
```bash
python3 -m news_crawler.international_news.cli config --site "网站名" --interval 7200
```

### Q: 如何查看爬取是否成功？

A: 使用 stats 命令查看统计信息：
```bash
python3 -m news_crawler.international_news.cli stats --days 7 --history
```

### Q: 爬取失败怎么办？

A: 检查：
1. 网络连接是否正常
2. 目标网站是否可访问
3. 是否被网站反爬虫机制拦截
4. 查看错误日志获取详细信息

### Q: 如何停止持续扫描？

A: 按 Ctrl+C 停止程序

---

**如需帮助，请查阅完整文档或提交 Issue！**
