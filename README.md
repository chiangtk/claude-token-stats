# Claude Code Token Stats

Real-time token usage monitoring for Claude Code - Web UI version

**Current Version: v1.1.0**

## Quick Start

```bash
# Navigate to project directory
cd ~/Downloads/claude-token-stats

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Then visit: http://localhost:5000

## Features

- 📊 Overall statistics overview (input/output/cache/cost)
- 🔢 API request count (includes all API calls)
- 📅 Today's real-time stats panel
- 🤖 Detailed usage by model
- 📈 Daily token usage trend chart
- 📊 Activity statistics (messages/tool calls)
- 🔄 Auto-refresh every 30 seconds
- 💰 Estimated cost calculation

## Changelog

### v1.1.0
- Added today's real-time stats panel
- Fixed API request count (now includes all API calls)
- Added version display in UI and API

### v1.0.0
- Initial release
- Basic token statistics functionality

## Data Source

Data is read from Claude Code session files:
```
~/.claude/projects/*/*.jsonl
```

## License

MIT License
