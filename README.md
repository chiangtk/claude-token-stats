# Claude Code Token Stats

实时查看 Claude Code 的 token 消耗统计 - Web UI 版本

**当前版本: v1.1.0**

## 快速启动

```bash
# 进入项目目录
cd ~/下载/claude-token-stats

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

然后访问: http://localhost:5000

## 功能

- 📊 总体统计概览（输入/输出/缓存/费用）
- 🔢 API 请求次数统计（包含所有 API 调用）
- 📅 今日实时统计面板
- 🤖 各模型详细使用情况
- 📈 每日 Token 使用趋势图
- 📊 活动统计（消息数/工具调用）
- 🔄 自动每30秒刷新
- 💰 预估费用计算

## 更新日志

### v1.1.0
- 新增今日实时统计面板
- 修复 API 请求次数统计（现在包含所有 API 调用）
- 添加版本号显示

### v1.0.0
- 初始版本
- 基础 token 统计功能

## 数据来源

数据来自 Claude Code 自动维护的 session 文件:
```
~/.claude/projects/*/*.jsonl
```
