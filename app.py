#!/usr/bin/env python3
"""
Claude Code Token Stats - Web UI
实时查看 Claude Code 的 token 消耗统计
"""

import json
import os
import glob
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

STATS_FILE = Path.home() / ".claude" / "stats-cache.json"
PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Claude 定价 (USD per 1M tokens) - 2025年价格
PRICING = {
    "claude-sonnet-4-6": {
        "input": 3.00,
        "output": 15.00,
        "cache_read": 0.30,
        "cache_write": 3.75,
    },
    "claude-opus-4-6": {
        "input": 15.00,
        "output": 75.00,
        "cache_read": 1.50,
        "cache_write": 18.75,
    },
    "claude-haiku-4-5-20251001": {
        "input": 0.80,
        "output": 4.00,
        "cache_read": 0.08,
        "cache_write": 1.00,
    },
}

MODEL_NAMES = {
    "claude-sonnet-4-6": "Sonnet 4.6",
    "claude-opus-4-6": "Opus 4.6",
    "claude-haiku-4-5-20251001": "Haiku 4.5",
}


def format_number(n):
    return f"{n:,}"


def format_tokens(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def calculate_cost(model, usage):
    pricing = PRICING.get(model, PRICING["claude-sonnet-4-6"])
    input_cost = (usage.get("inputTokens", 0) / 1_000_000) * pricing["input"]
    output_cost = (usage.get("outputTokens", 0) / 1_000_000) * pricing["output"]
    cache_read_cost = (usage.get("cacheReadInputTokens", 0) / 1_000_000) * pricing["cache_read"]
    cache_write_cost = (usage.get("cacheCreationInputTokens", 0) / 1_000_000) * pricing["cache_write"]
    return {
        "input": input_cost,
        "output": output_cost,
        "cache_read": cache_read_cost,
        "cache_write": cache_write_cost,
        "total": input_cost + output_cost + cache_read_cost + cache_write_cost,
    }


def get_stats():
    if not STATS_FILE.exists():
        return None
    with open(STATS_FILE, "r") as f:
        return json.load(f)


def get_realtime_usage():
    """从 session 文件中实时计算 token 使用量"""
    total_input = 0
    total_output = 0
    total_cache_read = 0
    total_cache_write = 0
    total_requests = 0
    total_api_calls = 0  # 所有 API 调用次数（包括无 token 的）
    daily_stats = {}  # 按日期统计

    # 遍历所有项目的 session 文件
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl_file in project_dir.glob("*.jsonl"):
            try:
                with open(jsonl_file, "r") as f:
                    for line in f:
                        try:
                            data = json.loads(line)
                            usage = data.get("message", {}).get("usage", {})
                            if usage:
                                input_t = usage.get("input_tokens", 0)
                                output_t = usage.get("output_tokens", 0)
                                cache_read = usage.get("cache_read_input_tokens", 0)
                                cache_write = usage.get("cache_creation_input_tokens", 0)

                                # 统计所有 API 调用
                                total_api_calls += 1

                                # 统计 token
                                total_input += input_t
                                total_output += output_t
                                total_cache_read += cache_read
                                total_cache_write += cache_write

                                # 只统计有实际 token 的请求
                                if input_t > 0 or output_t > 0:
                                    total_requests += 1

                                # 获取日期
                                timestamp = data.get("timestamp", "")
                                if timestamp:
                                    try:
                                        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                                        date_str = dt.strftime("%Y-%m-%d")
                                        if date_str not in daily_stats:
                                            daily_stats[date_str] = {
                                                "tokens": 0,
                                                "requests": 0,
                                                "apiCalls": 0,
                                                "input": 0,
                                                "output": 0,
                                            }
                                        daily_stats[date_str]["tokens"] += input_t + output_t
                                        daily_stats[date_str]["apiCalls"] += 1
                                        daily_stats[date_str]["input"] += input_t
                                        daily_stats[date_str]["output"] += output_t
                                        if input_t > 0 or output_t > 0:
                                            daily_stats[date_str]["requests"] += 1
                                    except:
                                        pass
                        except json.JSONDecodeError:
                            continue
            except Exception:
                continue

    return {
        "inputTokens": total_input,
        "outputTokens": total_output,
        "cacheReadInputTokens": total_cache_read,
        "cacheCreationInputTokens": total_cache_write,
        "totalTokens": total_input + total_output,
        "totalRequests": total_requests,
        "totalApiCalls": total_api_calls,
        "dailyStats": daily_stats,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def api_stats():
    data = get_stats()

    # 获取实时数据
    realtime = get_realtime_usage()

    model_usage = data.get("modelUsage", {}) if data else {}
    models = []
    total_input = realtime["inputTokens"]
    total_output = realtime["outputTokens"]
    total_cache_read = realtime["cacheReadInputTokens"]
    total_cache_write = realtime["cacheCreationInputTokens"]
    total_requests = realtime["totalRequests"]
    total_api_calls = realtime["totalApiCalls"]
    total_cost = 0

    for model, usage in model_usage.items():
        input_tokens = usage.get("inputTokens", 0)
        output_tokens = usage.get("outputTokens", 0)
        cache_read = usage.get("cacheReadInputTokens", 0)
        cache_write = usage.get("cacheCreationInputTokens", 0)

        cost = calculate_cost(model, usage)
        total_cost += cost["total"]

        models.append({
            "name": MODEL_NAMES.get(model, model),
            "id": model,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "cacheReadInputTokens": cache_read,
            "cacheCreationInputTokens": cache_write,
            "cost": cost,
        })

    # 计算实时费用（假设使用 Sonnet 定价）
    realtime_cost = (
        (total_input / 1_000_000) * 3.00 +
        (total_output / 1_000_000) * 15.00 +
        (total_cache_read / 1_000_000) * 0.30 +
        (total_cache_write / 1_000_000) * 3.75
    )

    # 从实时数据生成每日统计
    daily_stats = realtime.get("dailyStats", {})
    daily_chart = []
    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        daily_chart.append({
            "date": date,
            "total": stats["tokens"],
            "requests": stats["requests"],
            "apiCalls": stats["apiCalls"],
            "input": stats["input"],
            "output": stats["output"],
        })

    # 活动数据也从实时数据生成
    activity_chart = []
    for date in sorted(daily_stats.keys()):
        stats = daily_stats[date]
        activity_chart.append({
            "date": date,
            "messages": stats["requests"],
            "apiCalls": stats["apiCalls"],
            "sessions": 1,
            "toolCalls": 0,
        })

    return jsonify({
        "firstSession": data.get("firstSessionDate", "") if data else "",
        "totalSessions": data.get("totalSessions", 0) if data else 0,
        "totalMessages": data.get("totalMessages", 0) if data else 0,
        "totalRequests": total_requests,
        "totalApiCalls": total_api_calls,
        "models": models,
        "totals": {
            "inputTokens": total_input,
            "outputTokens": total_output,
            "cacheReadInputTokens": total_cache_read,
            "cacheCreationInputTokens": total_cache_write,
            "totalTokens": total_input + total_output,
            "totalCost": realtime_cost,
        },
        "dailyTokens": daily_chart,
        "dailyActivity": activity_chart,
        "lastUpdated": datetime.now().isoformat(),
        "dataSource": "realtime",
    })


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Claude Token Stats Web UI")
    print("=" * 50)
    print(f"📁 数据源: {STATS_FILE}")
    print(f"🌐 访问地址: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
