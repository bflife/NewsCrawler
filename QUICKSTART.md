# 快速开始 - 新闻爬虫调度系统

## 新功能速览

本次更新为NewsCrawler项目增加了以下核心功能：

✅ **国家/地区分类** - 支持200+全球新闻网站，按国家地区分类管理  
✅ **定时调度** - 自定义时间间隔，自动爬取新闻  
✅ **数据库存储** - SQLite存储爬取历史和文章数据  
✅ **命令行工具** - 完整的任务管理CLI  
✅ **通用爬虫框架** - 轻松扩展新的新闻源  

## 5分钟快速上手

### 1. 测试基本功能

```bash
# 运行测试脚本，验证系统是否正常
uv run python test_scheduler.py
```

### 2. 初始化任务

```bash
# 从配置文件加载200+新闻源，创建爬取任务
uv run python scheduler_cli.py init --interval 60
```

### 3. 查看任务

```bash
# 查看所有任务
uv run python scheduler_cli.py list

# 查看所有国家/地区
uv run python scheduler_cli.py countries

# 按国家查看任务
uv run python scheduler_cli.py list --country 台湾
uv run python scheduler_cli.py list --country 香港
uv run python scheduler_cli.py list --country 日本
```

### 4. 手动测试爬取

```bash
# 手动爬取一个新闻源测试
uv run python scheduler_cli.py run --source-id zaobao

# 查看爬取结果
uv run python scheduler_cli.py history --source-id zaobao
```

### 5. 启动调度器

```bash
# 启动后台调度器（每分钟自动检查任务）
uv run python scheduler_cli.py start
```

按 `Ctrl+C` 停止调度器。

## 支持的国家和地区

### 亚洲
- 🇨🇳 **中国**: 香港(20+)、台湾(17+)、澳门(10+)
- 🇯🇵 **日本**: NHK、朝日新闻、读卖新闻等18+网站
- 🇰🇷 **韩国**: 韩联社、朝鲜日报等
- 🇸🇬 **新加坡**: 联合早报
- 🇲🇾 **马来西亚**: 星洲日报、南洋商报等10+网站

### 欧美
- 🇺🇸 **美国**: CNN、纽约时报、华尔街日报等40+网站
- 🇬🇧 **英国**: BBC、路透社、金融时报等8+网站
- 🇫🇷 **法国**: 法新社、世界报等5+网站
- 🇩🇪 **德国**: 德国之声
- 🇷🇺 **俄罗斯**: 俄罗斯卫星通讯社等4+网站

### 其他
- 🇦🇺 澳大利亚、🇳🇿 新西兰、🇮🇳 印度、🇻🇳 越南等

## 常用命令

```bash
# 查看统计信息
uv run python scheduler_cli.py stats

# 启用/禁用任务
uv run python scheduler_cli.py enable --source-id zaobao
uv run python scheduler_cli.py disable --source-id zaobao

# 设置任务间隔（分钟）
uv run python scheduler_cli.py set-interval --source-id zaobao --interval 120

# 查看爬取历史
uv run python scheduler_cli.py history --limit 20

# 查看帮助
uv run python scheduler_cli.py --help
```

## 文档

- **详细文档**: [SCHEDULER_README.md](SCHEDULER_README.md)
- **使用示例**: `uv run python scheduler_examples.py`
- **原始文档**: [README.md](README.md)

## 项目结构

```
news_crawler/
├── config/
│   └── news_sources.json      # 200+新闻源配置
├── scheduler/                  # 调度器核心
│   ├── models.py              # 数据模型
│   ├── database.py            # SQLite数据库
│   └── scheduler.py           # 调度器
├── generic/                   # 通用爬虫基类
├── sites/                     # 具体网站爬虫
└── ...

scheduler_cli.py               # 命令行工具
scheduler_examples.py          # 使用示例
test_scheduler.py             # 快速测试
SCHEDULER_README.md           # 详细文档
```

## 注意事项

⚠️ **本项目仅供学习和研究使用**

- ✅ 遵守目标网站的robots.txt
- ✅ 设置合理的爬取间隔（建议60分钟以上）
- ✅ 控制爬取数量，避免对服务器造成压力
- ❌ 不得用于商业用途
- ❌ 不得进行大规模爬取

## 问题反馈

如有问题或建议，请提交 [Issue](https://github.com/NanmiCoder/NewsCrawler/issues)

## 许可证

本项目遵循原项目许可证，仅供学习和研究使用。
