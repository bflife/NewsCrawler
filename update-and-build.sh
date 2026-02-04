#!/bin/bash
# NewsCrawler v3.0 - 快速更新和构建脚本

set -e  # 遇到错误立即退出

echo "================================================================================"
echo "🔧 NewsCrawler v3.0 - 快速更新和构建"
echo "================================================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查当前目录
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是 NewsCrawler 项目根目录${NC}"
    echo "请先 cd 到 NewsCrawler 目录"
    exit 1
fi

echo -e "${YELLOW}步骤 1/6: 检查当前版本...${NC}"
CURRENT_VERSION=$(git log --oneline -1 2>/dev/null || echo "unknown")
echo "当前版本: $CURRENT_VERSION"
echo ""

echo -e "${YELLOW}步骤 2/6: 拉取最新代码...${NC}"
git fetch origin
git reset --hard origin/main
echo -e "${GREEN}✓ 代码已更新${NC}"
echo ""

NEW_VERSION=$(git log --oneline -1)
echo "新版本: $NEW_VERSION"
echo ""

echo -e "${YELLOW}步骤 3/6: 验证关键文件...${NC}"

# 验证 SchedulerManager.vue
if grep -q "const activeSchedulerTab" news-extractor-ui/frontend/src/components/SchedulerManager.vue; then
    echo -e "${GREEN}✓ SchedulerManager.vue 正确${NC}"
else
    echo -e "${RED}❌ SchedulerManager.vue 仍然是旧版本${NC}"
    exit 1
fi

# 验证 ResultViewerNew.vue
if grep -q "const activeResultTab" news-extractor-ui/frontend/src/components/ResultViewerNew.vue; then
    echo -e "${GREEN}✓ ResultViewerNew.vue 正确${NC}"
else
    echo -e "${RED}❌ ResultViewerNew.vue 仍然是旧版本${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}步骤 4/6: 停止现有容器...${NC}"
docker compose down -v 2>/dev/null || true
echo -e "${GREEN}✓ 容器已停止${NC}"
echo ""

echo -e "${YELLOW}步骤 5/6: 清理 Docker 缓存...${NC}"
docker system prune -af
echo -e "${GREEN}✓ 缓存已清理${NC}"
echo ""

echo -e "${YELLOW}步骤 6/6: 构建并启动服务...${NC}"
docker compose up -d --build

echo ""
echo "================================================================================"
echo -e "${GREEN}🎉 更新和构建完成！${NC}"
echo "================================================================================"
echo ""
echo "📍 访问地址："
echo "   🌐 Frontend: http://localhost:8080"
echo "   🔧 Backend:  http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📊 查看状态："
echo "   docker compose ps"
echo ""
echo "📝 查看日志："
echo "   docker compose logs -f"
echo ""
echo "================================================================================"
