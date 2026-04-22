# Development Roadmap

This document outlines potential improvements and future development plans for Claude Code Token Stats.

## Current Version: v1.2.0

---

## 🔴 High Priority

### 1. Data Persistence & History
**Problem:** Currently reads from session files each time, which can be slow for large datasets.

**Solutions:**
- Add SQLite database for caching historical data
- Implement incremental updates instead of full re-scan
- Add data export functionality (CSV, JSON)

```python
# Example: SQLite caching
import sqlite3
conn = sqlite3.connect('~/.claude/token_cache.db')
# Store daily stats, query efficiently
```

### 2. Cost Calculation Accuracy
**Problem:** Cost estimation uses fixed Sonnet pricing for all models.

**Solutions:**
- Detect actual model used per request
- Apply correct pricing per model
- Support custom pricing configuration

```python
# Model-specific pricing
PRICING = {
    "glm-5.1": {"input": 0.5, "output": 2.0},  # Example pricing
    # ... load from config file
}
```

### 3. Error Handling & Resilience
**Problem:** Network errors, missing files, corrupt data not handled gracefully.

**Solutions:**
- Add retry logic for network requests
- Validate JSON data before parsing
- Show user-friendly error messages
- Add health check endpoint

---

## 🟡 Medium Priority

### 4. Authentication & Security
**Current:** No authentication, anyone can access the dashboard.

**Improvements:**
- Add basic authentication (username/password)
- Support API key authentication
- Add rate limiting
- HTTPS support

```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Verify against config
    pass
```

### 5. Real-time Updates
**Current:** Polls every 30 seconds.

**Improvements:**
- WebSocket support for instant updates
- Server-Sent Events (SSE)
- Show "live" indicator when receiving data

```javascript
// WebSocket example
const ws = new WebSocket('ws://localhost:5000/ws');
ws.onmessage = (event) => updateStats(JSON.parse(event.data));
```

### 6. Advanced Analytics
**New Features:**
- Hourly/daily/weekly/monthly breakdown
- Token usage per project
- Token usage per conversation type
- Predictive cost forecasting
- Usage anomalies detection

### 7. Dashboard Customization
**Current:** Fixed layout.

**Improvements:**
- Drag-and-drop widget arrangement
- Hide/show specific metrics
- Custom date range selection
- Dark/light theme toggle (currently dark only)
- Save preferences to localStorage

---

## 🟢 Low Priority / Nice to Have

### 8. Multi-user Support
- User accounts with personal dashboards
- Team/organization support
- Usage quotas per user

### 9. Notifications & Alerts
- Email notifications for budget thresholds
- Webhook support for external integrations
- Slack/Discord notifications

```python
# Example: Budget alert
if current_cost > budget_threshold * 0.8:
    send_alert("80% of budget used!")
```

### 10. API Enhancements
- RESTful API documentation (OpenAPI/Swagger)
- GraphQL support for flexible queries
- API versioning

### 11. Mobile Support
- Responsive design improvements
- Native mobile app (React Native / Flutter)
- Push notifications

### 12. Historical Comparisons
- Compare usage between time periods
- Year-over-year analysis
- Trend visualization

---

## 🛠️ Technical Improvements

### Performance
- [ ] Implement lazy loading for large datasets
- [ ] Add caching headers for static assets
- [ ] Optimize JSON parsing (use orjson)
- [ ] Add request compression (gzip)

### Code Quality
- [ ] Add unit tests (pytest)
- [ ] Add integration tests
- [ ] Add type hints (mypy)
- [ ] Add pre-commit hooks
- [ ] Improve error logging

### DevOps
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Environment configuration (.env support)
- [ ] Logging to file with rotation

```dockerfile
# Dockerfile example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 📋 Feature Requests

### User-Requested Features
| Feature | Priority | Status |
|---------|----------|--------|
| Chinese/English toggle | High | ✅ Done |
| Today's stats panel | High | ✅ Done |
| All models display | High | ✅ Done |
| Cost per model | Medium | 🔜 Planned |
| Export data | Medium | 🔜 Planned |
| Budget alerts | Low | 📋 Backlog |

---

## 🗓️ Release Timeline

| Version | Target Date | Features |
|---------|-------------|----------|
| v1.3.0 | TBD | Cost per model, Export data |
| v1.4.0 | TBD | Authentication, WebSocket |
| v2.0.0 | TBD | Database backend, Multi-user |

---

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/chiangtk/claude-token-stats.git
cd claude-token-stats

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings for functions
- Keep functions under 50 lines

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Web Browser                        │
│  ┌─────────────────────────────────────────────┐   │
│  │           Frontend (HTML/JS/CSS)             │   │
│  │  - Chart.js for visualizations               │   │
│  │  - i18n for translations                     │   │
│  │  - Auto-refresh every 30s                    │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────▼──────────────────────────────┐
│                Flask Backend                         │
│  ┌─────────────────────────────────────────────┐   │
│  │  Routes:                                     │   │
│  │  - GET /           → Dashboard page          │   │
│  │  - GET /api/stats  → JSON statistics         │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Data Processing:                            │   │
│  │  - Parse session files (.jsonl)              │   │
│  │  - Calculate token usage                     │   │
│  │  - Compute costs                             │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │ File I/O
┌──────────────────────▼──────────────────────────────┐
│           Claude Code Data Files                     │
│  ~/.claude/                                          │
│  ├── stats-cache.json (legacy)                       │
│  └── projects/                                       │
│      └── */*.jsonl (session files)                   │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration Options (Planned)

```yaml
# config.yaml (planned)
server:
  host: "0.0.0.0"
  port: 5000
  debug: false

auth:
  enabled: true
  username: "admin"
  password_hash: "..."

pricing:
  claude-sonnet-4-6:
    input: 3.00
    output: 15.00
  glm-5.1:
    input: 0.50
    output: 2.00

alerts:
  budget_threshold: 100  # USD
  email: "user@example.com"

refresh_interval: 30  # seconds
```

---

## 📝 Notes

- This project is designed for local use with Claude Code CLI
- Data is read from local session files, no external API calls
- Cost estimates are approximate; actual costs may vary
- For production use, consider adding authentication

---

*Last updated: 2026-04-22*
