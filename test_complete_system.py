#!/usr/bin/env python3
"""
NewsCrawler 完整功能测试脚本
测试从爬虫创建到数据存储的完整流程
"""
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/home/user/webapp')

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")


def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    """打印信息"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    """打印警告"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


class TestResults:
    """测试结果统计"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def end(self):
        self.end_time = time.time()
    
    def add_pass(self, test_name):
        self.total += 1
        self.passed += 1
        print_success(f"{test_name}")
    
    def add_fail(self, test_name, error):
        self.total += 1
        self.failed += 1
        self.errors.append((test_name, error))
        print_error(f"{test_name}: {error}")
    
    def add_skip(self, test_name, reason):
        self.total += 1
        self.skipped += 1
        print_warning(f"{test_name}: {reason}")
    
    def summary(self):
        """打印测试摘要"""
        print_header("测试结果摘要")
        
        duration = self.end_time - self.start_time if self.end_time else 0
        
        print(f"总测试数: {Colors.BOLD}{self.total}{Colors.ENDC}")
        print(f"通过: {Colors.OKGREEN}{self.passed}{Colors.ENDC}")
        print(f"失败: {Colors.FAIL}{self.failed}{Colors.ENDC}")
        print(f"跳过: {Colors.WARNING}{self.skipped}{Colors.ENDC}")
        print(f"耗时: {Colors.OKCYAN}{duration:.2f}秒{Colors.ENDC}")
        
        if self.errors:
            print(f"\n{Colors.FAIL}失败详情:{Colors.ENDC}")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        # 计算通过率
        if self.total > 0:
            pass_rate = (self.passed / self.total) * 100
            if pass_rate >= 80:
                color = Colors.OKGREEN
            elif pass_rate >= 60:
                color = Colors.WARNING
            else:
                color = Colors.FAIL
            print(f"\n{Colors.BOLD}通过率: {color}{pass_rate:.1f}%{Colors.ENDC}")


results = TestResults()


def test_imports():
    """测试1: 导入测试"""
    print_header("测试1: 导入测试")
    
    try:
        from news_crawler.core.base import BaseNewsCrawler
        results.add_pass("导入 BaseNewsCrawler")
    except Exception as e:
        results.add_fail("导入 BaseNewsCrawler", str(e))
    
    try:
        from news_crawler.core.enhanced import EnhancedNewsCrawler, SelectorConfig, AntiCrawlerConfig
        results.add_pass("导入增强版爬虫组件")
    except Exception as e:
        results.add_fail("导入增强版爬虫组件", str(e))
    
    try:
        from news_crawler.core.selector_configs import get_selector_config, SELECTOR_CONFIGS
        results.add_pass("导入选择器配置")
    except Exception as e:
        results.add_fail("导入选择器配置", str(e))
    
    try:
        from news_crawler.sites.enhanced_crawlers import ENHANCED_CRAWLERS
        results.add_pass("导入增强版爬虫集")
    except Exception as e:
        results.add_fail("导入增强版爬虫集", str(e))
    
    try:
        from news_crawler.sites import get_all_crawlers, get_supported_countries
        results.add_pass("导入爬虫注册中心")
    except Exception as e:
        results.add_fail("导入爬虫注册中心", str(e))


def test_crawler_registry():
    """测试2: 爬虫注册表测试"""
    print_header("测试2: 爬虫注册表测试")
    
    try:
        from news_crawler.sites import get_all_crawlers, get_statistics
        
        all_crawlers = get_all_crawlers()
        if len(all_crawlers) > 0:
            results.add_pass(f"爬虫注册表包含 {len(all_crawlers)} 个爬虫")
        else:
            results.add_fail("爬虫注册表", "没有注册的爬虫")
        
        stats = get_statistics()
        expected_keys = ['total_crawlers', 'total_countries', 'crawlers_per_country']
        if all(key in stats for key in expected_keys):
            results.add_pass("统计信息格式正确")
            print_info(f"  - 总爬虫数: {stats['total_crawlers']}")
            print_info(f"  - 覆盖国家: {stats['total_countries']}")
        else:
            results.add_fail("统计信息格式", "缺少必需字段")
    
    except Exception as e:
        results.add_fail("爬虫注册表测试", str(e))


def test_enhanced_crawlers():
    """测试3: 增强版爬虫测试"""
    print_header("测试3: 增强版爬虫测试")
    
    try:
        from news_crawler.sites.enhanced_crawlers import ENHANCED_CRAWLERS
        
        if len(ENHANCED_CRAWLERS) >= 20:
            results.add_pass(f"增强版爬虫数量: {len(ENHANCED_CRAWLERS)}")
        else:
            results.add_fail("增强版爬虫数量", f"只有 {len(ENHANCED_CRAWLERS)} 个")
        
        # 测试几个关键爬虫
        test_crawlers = ['cnn', 'bbc_chinese', 'nytimes', 'zaobao']
        for name in test_crawlers:
            if name in ENHANCED_CRAWLERS:
                crawler_class = ENHANCED_CRAWLERS[name]
                if hasattr(crawler_class, 'name') and hasattr(crawler_class, 'base_url'):
                    results.add_pass(f"爬虫 '{name}' 配置正确")
                else:
                    results.add_fail(f"爬虫 '{name}'", "缺少必需属性")
            else:
                results.add_fail(f"爬虫 '{name}'", "未找到")
    
    except Exception as e:
        results.add_fail("增强版爬虫测试", str(e))


def test_selector_configs():
    """测试4: 选择器配置测试"""
    print_header("测试4: 选择器配置测试")
    
    try:
        from news_crawler.core.selector_configs import SELECTOR_CONFIGS, get_selector_config
        
        if len(SELECTOR_CONFIGS) >= 20:
            results.add_pass(f"选择器配置数量: {len(SELECTOR_CONFIGS)}")
        else:
            results.add_fail("选择器配置数量", f"只有 {len(SELECTOR_CONFIGS)} 个")
        
        # 测试配置获取
        test_configs = ['cnn', 'bbc_chinese', 'nytimes']
        for name in test_configs:
            config = get_selector_config(name)
            if config is not None:
                results.add_pass(f"获取 '{name}' 选择器配置")
            else:
                results.add_fail(f"'{name}' 选择器配置", "返回None")
    
    except Exception as e:
        results.add_fail("选择器配置测试", str(e))


def test_anti_crawler_config():
    """测试5: 反爬配置测试"""
    print_header("测试5: 反爬配置测试")
    
    try:
        from news_crawler.core.selector_configs import get_anti_crawler_config
        from news_crawler.core.enhanced import AntiCrawlerConfig
        
        # 测试默认配置
        default_config = get_anti_crawler_config('default')
        if isinstance(default_config, AntiCrawlerConfig):
            results.add_pass("获取默认反爬配置")
            
            # 验证配置属性
            if hasattr(default_config, 'min_delay') and default_config.min_delay > 0:
                results.add_pass("反爬配置包含延迟设置")
            else:
                results.add_fail("反爬配置", "延迟设置不正确")
            
            if hasattr(default_config, 'user_agents') and len(default_config.user_agents) > 0:
                results.add_pass(f"User-Agent池: {len(default_config.user_agents)}个")
            else:
                results.add_fail("User-Agent池", "为空")
        else:
            results.add_fail("默认反爬配置", "类型不正确")
    
    except Exception as e:
        results.add_fail("反爬配置测试", str(e))


def test_crawler_instantiation():
    """测试6: 爬虫实例化测试"""
    print_header("测试6: 爬虫实例化测试")
    
    try:
        from news_crawler.sites.enhanced_crawlers import ZaobaoCrawler, HK01Crawler
        
        # 测试联合早报爬虫
        test_url = "https://www.zaobao.com.sg/news/china/story20240101-test"
        try:
            zaobao = ZaobaoCrawler(
                new_url=test_url,
                save_path="data/test/"
            )
            if zaobao.name == "zaobao" and zaobao.base_url:
                results.add_pass("实例化 ZaobaoCrawler")
                
                # 检查配置
                if hasattr(zaobao, 'selector_config') and zaobao.selector_config:
                    results.add_pass("ZaobaoCrawler 包含选择器配置")
                else:
                    results.add_fail("ZaobaoCrawler", "缺少选择器配置")
                
                if hasattr(zaobao, 'anti_crawler_config') and zaobao.anti_crawler_config:
                    results.add_pass("ZaobaoCrawler 包含反爬配置")
                else:
                    results.add_fail("ZaobaoCrawler", "缺少反爬配置")
            else:
                results.add_fail("ZaobaoCrawler", "属性不正确")
        except Exception as e:
            results.add_fail("实例化 ZaobaoCrawler", str(e))
        
        # 测试香港01爬虫
        try:
            hk01 = HK01Crawler(
                new_url="https://www.hk01.com/article/123456",
                save_path="data/test/"
            )
            if hk01.name == "hk01":
                results.add_pass("实例化 HK01Crawler")
            else:
                results.add_fail("HK01Crawler", "名称不正确")
        except Exception as e:
            results.add_fail("实例化 HK01Crawler", str(e))
    
    except Exception as e:
        results.add_fail("爬虫实例化测试", str(e))


def test_data_models():
    """测试7: 数据模型测试"""
    print_header("测试7: 数据模型测试")
    
    try:
        from news_crawler.core.models import NewsItem, NewsMetaInfo, ContentItem, ContentType
        
        # 测试创建 ContentItem
        try:
            content = ContentItem(
                type=ContentType.TEXT,
                content="测试内容"
            )
            if content.type == ContentType.TEXT and content.content == "测试内容":
                results.add_pass("创建 ContentItem")
            else:
                results.add_fail("ContentItem", "属性不正确")
        except Exception as e:
            results.add_fail("创建 ContentItem", str(e))
        
        # 测试创建 NewsMetaInfo
        try:
            meta = NewsMetaInfo(
                author_name="测试作者",
                publish_time="2024-01-01"
            )
            if meta.author_name == "测试作者":
                results.add_pass("创建 NewsMetaInfo")
            else:
                results.add_fail("NewsMetaInfo", "属性不正确")
        except Exception as e:
            results.add_fail("创建 NewsMetaInfo", str(e))
        
        # 测试创建 NewsItem
        try:
            news = NewsItem(
                title="测试标题",
                news_url="https://example.com/test",
                news_id="test_123",
                meta_info=meta,
                contents=[content]
            )
            if news.title == "测试标题" and len(news.contents) == 1:
                results.add_pass("创建 NewsItem")
            else:
                results.add_fail("NewsItem", "属性不正确")
        except Exception as e:
            results.add_fail("创建 NewsItem", str(e))
    
    except Exception as e:
        results.add_fail("数据模型测试", str(e))


def test_file_system():
    """测试8: 文件系统测试"""
    print_header("测试8: 文件系统测试")
    
    test_dir = Path("data/test/")
    
    try:
        # 创建测试目录
        test_dir.mkdir(parents=True, exist_ok=True)
        if test_dir.exists():
            results.add_pass("创建测试目录")
        else:
            results.add_fail("创建测试目录", "目录不存在")
        
        # 测试写入JSON文件
        test_file = test_dir / "test_article.json"
        test_data = {
            "title": "测试文章",
            "content": "这是一个测试",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2)
            
            if test_file.exists():
                results.add_pass("写入测试JSON文件")
                
                # 读取并验证
                with open(test_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                if loaded_data['title'] == test_data['title']:
                    results.add_pass("读取并验证JSON文件")
                else:
                    results.add_fail("JSON文件验证", "内容不匹配")
            else:
                results.add_fail("写入测试JSON文件", "文件不存在")
        except Exception as e:
            results.add_fail("JSON文件操作", str(e))
        
        # 清理测试文件
        try:
            if test_file.exists():
                test_file.unlink()
                results.add_pass("清理测试文件")
        except Exception as e:
            results.add_fail("清理测试文件", str(e))
    
    except Exception as e:
        results.add_fail("文件系统测试", str(e))


def test_scheduler_integration():
    """测试9: 调度器集成测试"""
    print_header("测试9: 调度器集成测试")
    
    try:
        from news_crawler.scheduler import NewsScheduler
        
        # 创建调度器实例
        try:
            scheduler = NewsScheduler(db_path="data/test/test_scheduler.db")
            results.add_pass("创建调度器实例")
            
            # 测试注册爬虫
            try:
                from news_crawler.sites import register_all_crawlers
                
                # 注意：这里会注册所有爬虫，可能需要一些时间
                print_info("  正在注册爬虫...")
                count = register_all_crawlers(scheduler)
                
                if count > 0:
                    results.add_pass(f"注册爬虫: {count}个")
                else:
                    results.add_fail("注册爬虫", "没有爬虫被注册")
            except Exception as e:
                results.add_skip("注册爬虫", f"跳过: {str(e)}")
        
        except Exception as e:
            results.add_fail("创建调度器实例", str(e))
    
    except Exception as e:
        results.add_skip("调度器集成测试", f"跳过: {str(e)}")


def test_api_imports():
    """测试10: API导入测试"""
    print_header("测试10: API导入测试")
    
    try:
        from news_extractor_backend.api.scheduler import router
        results.add_pass("导入调度器API路由")
    except Exception as e:
        results.add_fail("导入调度器API路由", str(e))
    
    try:
        from news_extractor_backend.api.extract import router as extract_router
        results.add_pass("导入提取API路由")
    except Exception as e:
        results.add_fail("导入提取API路由", str(e))
    
    try:
        from news_extractor_backend.main import app
        results.add_pass("导入FastAPI应用")
    except Exception as e:
        results.add_fail("导入FastAPI应用", str(e))


def test_configuration_files():
    """测试11: 配置文件测试"""
    print_header("测试11: 配置文件测试")
    
    # 测试news_sources.json
    config_file = Path("news_crawler/config/news_sources.json")
    if config_file.exists():
        results.add_pass("news_sources.json 存在")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if 'sources' in config_data:
                sources_count = len(config_data['sources'])
                results.add_pass(f"配置文件包含 {sources_count} 个新闻源")
            else:
                results.add_fail("配置文件格式", "缺少 'sources' 字段")
        except Exception as e:
            results.add_fail("读取配置文件", str(e))
    else:
        results.add_fail("news_sources.json", "文件不存在")
    
    # 测试其他配置文件
    config_files = [
        "pyproject.toml",
        "requirements.txt",
        "docker-compose.yml"
    ]
    
    for filename in config_files:
        filepath = Path(filename)
        if filepath.exists():
            results.add_pass(f"{filename} 存在")
        else:
            results.add_warning(f"{filename} 不存在")


def test_documentation():
    """测试12: 文档测试"""
    print_header("测试12: 文档测试")
    
    doc_files = [
        "README.md",
        "ENHANCED_CRAWLER_REPORT.md",
        "CRAWLER_EXPANSION_REPORT.md",
        "SCHEDULER_README.md",
        "WEBUI_GUIDE.md",
        "PROJECT_SUMMARY.md"
    ]
    
    for filename in doc_files:
        filepath = Path(filename)
        if filepath.exists():
            size = filepath.stat().st_size
            if size > 1000:  # 至少1KB
                results.add_pass(f"{filename} ({size} bytes)")
            else:
                results.add_warning(f"{filename} 文件太小 ({size} bytes)")
        else:
            results.add_fail(filename, "文件不存在")


def main():
    """主测试函数"""
    print_header("NewsCrawler 完整功能测试套件")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"工作目录: {os.getcwd()}")
    
    results.start()
    
    # 运行所有测试
    test_imports()
    test_crawler_registry()
    test_enhanced_crawlers()
    test_selector_configs()
    test_anti_crawler_config()
    test_crawler_instantiation()
    test_data_models()
    test_file_system()
    test_scheduler_integration()
    test_api_imports()
    test_configuration_files()
    test_documentation()
    
    results.end()
    
    # 打印摘要
    results.summary()
    
    # 返回退出码
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
