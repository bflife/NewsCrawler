# 国际新闻爬虫 (International News Crawler)

自动爬取全球主要新闻网站的新闻内容，支持定时扫描、更新检测和分类管理。

## 🌍 支持的国家/地区

本模块支持从以下国家/地区的主要新闻网站爬取内容：

### 东亚
- 🇯🇵 日本 (14个网站): 共同社、NHK、朝日新闻、读卖新闻等
- 🇰🇷 韩国 (4个网站): 韩联社、大纪元等
- 🇰🇵 朝鲜 (1个网站): 朝鲜日报

### 东南亚
- 🇲🇾 马来西亚 (10个网站): 星洲日报、光明日报、东方日报等
- 🇸🇬 新加坡 (2个网站): 联合早报、光明日报
- 🇻🇳 越南 (2个网站): 越南通讯社、越南之声
- 🇲🇲 缅甸 (1个网站): 缅甸民主之声

### 大中华
- 🇭🇰 香港 (21个网站): 苹果日报、南华早报、香港01等
- 🇲🇴 澳门 (12个网站): 澳门日报、力报、正报等
- 🇹🇼 台湾 (13个网站): 自由时报、联合报、中时电子报等

### 欧洲
- 🇬🇧 英国 (8个网站): 路透社、BBC、金融时报、卫报等
- 🇫🇷 法国 (5个网站): 法新社、世界报、费加罗报等
- 🇩🇪 德国 (1个网站): 德国之声
- 🇮🇪 爱尔兰 (1个网站): 开放杂志
- 🇷🇺 俄罗斯 (4个网站): 俄新社、卫星通讯社等

### 北美
- 🇺🇸 美国 (22个网站): 纽约时报、华尔街日报、CNN、美联社等

### 大洋洲
- 🇦🇺 澳大利亚 (3个网站): 澳广、每日电讯报等
- 🇳🇿 新西兰 (2个网站): 看中国、阿波罗网

### 南亚
- 🇮🇳 印度 (3个网站): 印度斯坦时报、印度教徒报、印度快报

### 其他
- 🇦🇿 阿塞拜疆 (3个网站)

**总计：超过 130 个国际新闻网站**

## ✨ 功能特性

- ✅ **分类管理** - 按国家/地区分类组织新闻网站
- ✅ **定时扫描** - 可配置的扫描间隔，自动检查更新
- ✅ **更新检测** - 智能识别新文章，避免重复爬取
- ✅ **通用爬虫** - 自适应多种网站结构的智能提取算法
- ✅ **并行处理** - 支持多线程并发爬取，提升效率
- ✅ **历史追踪** - SQLite 数据库记录爬取历史和统计
- ✅ **灵活配置** - 可针对每个网站配置扫描间隔和启用状态
- ✅ **命令行工具** - 完整的 CLI 工具，方便自动化部署

## 🚀 快速开始

### 安装依赖

```bash
# 进入项目目录
cd /home/user/webapp

# 使用 uv 安装依赖
uv sync
```

### 基本使用

```bash
# 1. 列出所有可用国家
uv run python -m news_crawler.international_news.cli list --countries

# 2. 列出所有可用地区
uv run python -m news_crawler.international_news.cli list --regions

# 3. 查看某个国家的所有网站
uv run python -m news_crawler.international_news.cli list --country 美国

# 4. 扫描所有网站(一次性)
uv run python -m news_crawler.international_news.cli scan --all --max-articles 5

# 5. 只扫描特定国家
uv run python -m news_crawler.international_news.cli scan --country 日本 --max-articles 5

# 6. 只扫描特定地区
uv run python -m news_crawler.international_news.cli scan --region 东亚 --max-articles 5

# 7. 启动持续扫描(每小时检查一次)
uv run python -m news_crawler.international_news.cli start --interval 3600

# 8. 查看爬取统计
uv run python -m news_crawler.international_news.cli stats --days 7 --history

# 9. 配置特定网站
uv run python -m news_crawler.international_news.cli config --site "BBC" --interval 7200 --enable
```

## 📖 使用指南

### 1. 列出网站

```bash
# 列出所有国家
uv run python -m news_crawler.international_news.cli list --countries

# 列出所有地区分组
uv run python -m news_crawler.international_news.cli list --regions

# 列出某个国家的网站
uv run python -m news_crawler.international_news.cli list --country 日本

# 列出某个地区的网站
uv run python -m news_crawler.international_news.cli list --region 东亚

# 包含已禁用的网站
uv run python -m news_crawler.international_news.cli list --country 美国 --all
```

### 2. 扫描网站

```bash
# 扫描所有网站
uv run python -m news_crawler.international_news.cli scan --all

# 扫描特定国家
uv run python -m news_crawler.international_news.cli scan --country 美国 --max-articles 10

# 扫描特定地区
uv run python -m news_crawler.international_news.cli scan --region 东亚 --max-articles 5

# 显示详细信息
uv run python -m news_crawler.international_news.cli scan --all --verbose --show-articles

# 自定义并发数
uv run python -m news_crawler.international_news.cli scan --all --workers 10
```

### 3. 持续扫描

```bash
# 启动持续扫描(默认每小时检查一次)
uv run python -m news_crawler.international_news.cli start --interval 3600

# 只扫描特定国家
uv run python -m news_crawler.international_news.cli start --country 日本 --interval 1800

# 只扫描特定地区
uv run python -m news_crawler.international_news.cli start --region 东亚 --interval 3600

# 自定义设置
uv run python -m news_crawler.international_news.cli start \
    --interval 7200 \
    --max-articles 20 \
    --workers 8
```

### 4. 查看统计

```bash
# 查看最近7天的统计
uv run python -m news_crawler.international_news.cli stats --days 7

# 查看统计并显示历史记录
uv run python -m news_crawler.international_news.cli stats --days 30 --history --limit 50
```

### 5. 配置网站

```bash
# 列出所有可配置的网站
uv run python -m news_crawler.international_news.cli config --list-sites

# 启用某个网站
uv run python -m news_crawler.international_news.cli config --site "BBC" --enable

# 禁用某个网站
uv run python -m news_crawler.international_news.cli config --site "CNN" --disable

# 设置扫描间隔(秒)
uv run python -m news_crawler.international_news.cli config --site "纽约时报" --interval 7200

# 同时设置多个参数
uv run python -m news_crawler.international_news.cli config --site "日经新闻" --enable --interval 3600
```

## 🔧 Python API 使用

### 基本爬取

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
    print(f"URL: {article['url']}")

# 爬取单篇文章
crawler_single = InternationalNewsCrawler(
    news_url="https://www.bbc.com/news/world-12345678",
    site_config={'name': 'BBC'}
)
news_item = crawler_single.run()
print(f"标题: {news_item.title}")
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
for site in us_sites:
    print(f"{site['site_name']}: {site['site_url']}")

# 获取需要扫描的网站
sites_to_scan = manager.get_sites_to_scan()
print(f"需要扫描 {len(sites_to_scan)} 个网站")

# 记录爬取历史
manager.record_crawl(
    site_name="BBC",
    site_url="https://www.bbc.com",
    country="英国",
    article_url="https://www.bbc.com/news/12345",
    article_title="Sample Article",
    status="success",
    article_count=1
)

# 查看统计
stats = manager.get_crawl_statistics(days=7)
print(f"成功率: {stats['success_rate']}")
print(f"总文章数: {stats['total_articles']}")
```

### 使用调度器

```python
from news_crawler.international_news import NewsScheduler, ConfigManager

# 初始化
manager = ConfigManager()
manager.load_site_configs()

scheduler = NewsScheduler(
    config_manager=manager,
    max_workers=5
)

# 一次性扫描所有网站
results = scheduler.scan_all_sites(max_articles_per_site=10)
print(f"扫描了 {len(results)} 个网站")
print(f"发现 {sum(r['new_articles'] for r in results)} 篇新文章")

# 扫描特定国家
results = scheduler.scan_all_sites(
    country="日本",
    max_articles_per_site=5,
    parallel=True
)

# 启动持续扫描
scheduler.start_continuous_scanning(
    check_interval=3600,  # 每小时检查
    max_articles_per_site=10
)
```

### 自定义回调

```python
from news_crawler.international_news import NewsScheduler, ConfigManager

def on_article_crawled(news_item, site_name, country):
    """当文章被爬取时的回调"""
    print(f"[{country}] {site_name}: {news_item.title}")
    # 可以在这里添加自定义处理逻辑
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

爬取的新闻内容保存在以下位置：

```
data/international_news/
├── {article_id_1}.json
├── {article_id_2}.json
└── ...
```

每个文章保存为标准的 JSON 格式：

```json
{
  "title": "文章标题",
  "news_url": "文章URL",
  "news_id": "文章ID",
  "meta_info": {
    "author_name": "作者",
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

爬取历史和配置存储在 SQLite 数据库：

```
data/international_news/crawl_history.db
```

包含以下表：
- `site_configs` - 网站配置
- `crawl_history` - 爬取历史
- `latest_articles` - 最新文章追踪

## ⚙️ 配置说明

### 扫描间隔

每个网站可以配置独立的扫描间隔(以秒为单位):

- 默认: 3600 秒 (1小时)
- 建议范围: 1800-7200 秒 (30分钟 - 2小时)
- 重要网站可设置更短间隔
- 不常更新的网站可设置更长间隔

### 并发设置

- `max_workers`: 并发线程数，默认 5
- 建议根据网络带宽和系统资源调整
- 过高可能导致被网站封禁
- 过低影响爬取效率

### 文章数量

- `max_articles_per_site`: 每个网站爬取的最大文章数
- 默认: 10 篇
- 建议: 5-20 篇之间
- 首次运行可设置较大值

## 🛠️ 高级功能

### 自定义网站配置

可以在代码中动态添加新网站：

```python
from news_crawler.international_news.configs.sites_config import NEWS_SITES_CONFIG

# 添加新网站
NEWS_SITES_CONFIG["新国家"] = [
    {
        "name": "新网站",
        "url": "https://example.com",
        "encoding": "utf-8",
        "type": "newspaper"
    }
]
```

### 扩展爬虫功能

继承 `InternationalNewsCrawler` 类可以自定义爬取逻辑：

```python
from news_crawler.international_news import InternationalNewsCrawler

class CustomNewsCrawler(InternationalNewsCrawler):
    def _extract_title(self, selector):
        # 自定义标题提取逻辑
        return selector.css('h1.custom-title::text').get() or super()._extract_title(selector)
    
    def _extract_main_content(self, selector):
        # 自定义内容提取逻辑
        # ...
        return contents
```

## 📝 注意事项

1. **遵守 robots.txt**: 爬取前请检查目标网站的 robots.txt 文件
2. **控制频率**: 避免过于频繁的请求，建议每个网站间隔至少 1-2 秒
3. **错误处理**: 网站结构可能变化，导致爬取失败，需定期检查
4. **法律合规**: 仅用于学习研究，不得用于商业用途
5. **网络环境**: 某些网站可能需要代理才能访问

## 🤝 贡献

欢迎贡献新的网站配置或改进爬取算法！

## 📄 许可

本项目仅供教育和研究使用。

---

**如有问题或建议，请提交 Issue！**
