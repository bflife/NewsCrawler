#!/usr/bin/env python3
"""
测试增强版新闻爬虫
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, '/home/user/webapp')

from news_crawler.sites.enhanced_crawlers import ENHANCED_CRAWLERS


def test_crawler(crawler_name: str, test_url: str):
    """测试单个爬虫"""
    print(f"\n{'='*80}")
    print(f"测试爬虫: {crawler_name}")
    print(f"测试URL: {test_url}")
    print(f"{'='*80}\n")
    
    try:
        # 获取爬虫类
        crawler_class = ENHANCED_CRAWLERS.get(crawler_name)
        if not crawler_class:
            print(f"❌ 爬虫 {crawler_name} 不存在")
            return False
        
        # 创建爬虫实例
        crawler = crawler_class(
            new_url=test_url,
            save_path="data/test/"
        )
        
        # 运行爬虫
        print("🔄 开始抓取...")
        news_item = crawler.run(persist=True)
        
        # 显示结果
        print(f"\n✅ 抓取成功!")
        print(f"标题: {news_item.title}")
        print(f"副标题: {news_item.subtitle or 'N/A'}")
        print(f"作者: {news_item.meta_info.author_name or 'N/A'}")
        print(f"发布时间: {news_item.meta_info.publish_time or 'N/A'}")
        print(f"内容块数量: {len(news_item.contents)}")
        print(f"文本段落: {len(news_item.texts)}")
        print(f"图片数量: {len(news_item.images)}")
        print(f"视频数量: {len(news_item.videos)}")
        print(f"保存路径: {crawler.get_save_json_path()}")
        
        # 显示前3段文本
        if news_item.texts:
            print(f"\n前3段内容预览:")
            for i, text in enumerate(news_item.texts[:3], 1):
                preview = text[:100] + "..." if len(text) > 100 else text
                print(f"  {i}. {preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ 抓取失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 增强版新闻爬虫测试")
    print(f"共有 {len(ENHANCED_CRAWLERS)} 个增强版爬虫可测试")
    
    # 测试用例
    test_cases = [
        # 美国
        # ('cnn', 'https://www.cnn.com/2024/01/01/world/example-article/index.html'),
        # ('nytimes_chinese', 'https://cn.nytimes.com/china/20240101/example-article/'),
        
        # 英国
        # ('bbc_chinese', 'https://www.bbc.com/zhongwen/simp/chinese-news-12345678'),
        
        # 日本  
        # ('nhk_news', 'http://www3.nhk.or.jp/news/html/20240101/k10012345671000.html'),
        
        # 中文
        # ('zaobao', 'https://www.zaobao.com.sg/news/china/story20240101-1234567'),
        # ('hk01', 'https://www.hk01.com/article/123456'),
        # ('ltn', 'https://news.ltn.com.tw/news/politics/breakingnews/1234567'),
    ]
    
    if not test_cases:
        print("\n⚠️  没有配置测试用例")
        print("请在代码中添加真实的新闻URL进行测试")
        print("\n示例:")
        print("test_cases = [")
        print("    ('bbc_chinese', 'https://www.bbc.com/zhongwen/simp/chinese-news-12345678'),")
        print("    ('zaobao', 'https://www.zaobao.com.sg/news/china/story20240101-1234567'),")
        print("]")
        return
    
    # 运行测试
    success_count = 0
    fail_count = 0
    
    for crawler_name, test_url in test_cases:
        result = test_crawler(crawler_name, test_url)
        if result:
            success_count += 1
        else:
            fail_count += 1
    
    # 汇总
    print(f"\n{'='*80}")
    print(f"测试完成")
    print(f"{'='*80}")
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {fail_count}")
    print(f"总计: {success_count + fail_count}")


if __name__ == "__main__":
    main()
