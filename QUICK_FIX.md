# 🚨 Docker 构建错误 - 快速修复指南

## 问题说明

您看到的错误：
```
Cannot redeclare block-scoped variable 'activeTab'
```

**原因**: 您使用的是旧版本代码（可能是从 NewsCrawler-v3.0 解压的），该版本尚未包含我们的修复。

---

## ✅ 快速修复（推荐）

### 方法 1: 使用一键脚本（最简单）

```bash
# 1. 进入项目目录
cd ~/NewsCrawler  # 或您的 NewsCrawler 目录

# 2. 如果目录不存在，先克隆
# cd ~
# git clone https://github.com/bflife/NewsCrawler.git
# cd NewsCrawler

# 3. 运行更新脚本
./update-and-build.sh
```

脚本会自动：
- ✅ 拉取最新代码
- ✅ 验证文件正确性
- ✅ 清理 Docker 缓存
- ✅ 重新构建服务

---

### 方法 2: 手动更新

```bash
# 1. 进入项目目录（如果不存在先克隆）
cd ~/NewsCrawler

# 2. 强制更新到最新版本
git fetch origin
git reset --hard origin/main

# 3. 验证版本（应该显示 1fd2649 或更新）
git log --oneline -1

# 4. 验证修复（应该显示 activeSchedulerTab）
grep "const activeSchedulerTab" news-extractor-ui/frontend/src/components/SchedulerManager.vue

# 5. 清理并重建
docker compose down -v
docker system prune -af
docker compose up -d --build
```

---

### 方法 3: 全新克隆

```bash
# 1. 删除旧目录
cd ~
rm -rf NewsCrawler NewsCrawler-v3.0

# 2. 克隆最新代码
git clone https://github.com/bflife/NewsCrawler.git
cd NewsCrawler

# 3. 构建
docker compose up -d --build
```

---

## 🔍 验证修复

### 检查代码版本
```bash
cd NewsCrawler
git log --oneline -1
```

**期望输出**（或更新的版本）:
```
1fd2649 feat: 添加一键更新和构建脚本
```

### 检查文件内容
```bash
# SchedulerManager.vue 应该使用 activeSchedulerTab
grep "const activeSchedulerTab" news-extractor-ui/frontend/src/components/SchedulerManager.vue

# ResultViewerNew.vue 应该使用 activeResultTab
grep "const activeResultTab" news-extractor-ui/frontend/src/components/ResultViewerNew.vue
```

---

## 🎯 构建成功标志

看到以下输出表示成功：

```
✓ built in XXXms
vite v4.x.x building for production...
✓ XX modules transformed.
dist/index.html
```

**不会再出现**：
```
Cannot redeclare block-scoped variable 'activeTab'
```

---

## 📊 访问服务

构建成功后访问：

- 🌐 **Frontend**: http://localhost:8080
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

---

## ❓ 常见问题

### Q: 脚本报错 "permission denied"
```bash
chmod +x update-and-build.sh
./update-and-build.sh
```

### Q: Git 提示有本地修改
```bash
git reset --hard HEAD
git pull origin main
```

### Q: Docker 缓存问题
```bash
docker compose down -v
docker system prune -af --volumes
docker builder prune -af
```

### Q: 仍然看到旧代码
确保您在正确的目录：
```bash
pwd  # 应该显示类似 /root/NewsCrawler 或 ~/NewsCrawler
# 不应该是 NewsCrawler-v3.0
```

---

## 📞 需要帮助？

如果按照上述步骤仍然失败：

1. 提供以下信息：
```bash
pwd
git log --oneline -1
grep "const active" news-extractor-ui/frontend/src/components/SchedulerManager.vue
docker compose version
```

2. 或查看详细故障排除指南：[DOCKER_BUILD_TROUBLESHOOTING.md](DOCKER_BUILD_TROUBLESHOOTING.md)

---

## ✅ 总结

**最快的修复方法**：
```bash
cd NewsCrawler
./update-and-build.sh
```

**如果没有 NewsCrawler 目录**：
```bash
git clone https://github.com/bflife/NewsCrawler.git
cd NewsCrawler
docker compose up -d --build
```

---

**重要**: 不要使用 `NewsCrawler-v3.0` 目录或旧的 tar.gz 文件，请始终从 GitHub 获取最新代码！
