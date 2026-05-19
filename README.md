# HIPS - Host Intrusion Prevention System

A comprehensive, cross-platform security monitoring and intrusion prevention system designed for FSKTM Data Centre with real-time threat detection, rule-based event matching, and a modern web-based dashboard.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Rules System](#rules-system)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Monitoring Components](#monitoring-components)
- [Frontend Pages](#frontend-pages)
- [Project Structure](#project-structure)
- [Development](#development)

---

## Overview

HIPS (Host Intrusion Prevention System) is a real-time security monitoring solution that:

- **Monitors** system activities across process execution, filesystem operations, network connections, and Windows registry changes
- **Detects** threats using YAML-based detection rules
- **Alerts** on suspicious activities with severity classifications (low, medium, high, critical)
- **Blocks** malicious processes and connections based on configured rules
- **Logs** all events to a local SQLite database for forensic analysis
- **Visualizes** security data through an interactive React-based dashboard with real-time WebSocket updates

---

## Architecture

HIPS follows a **client-server architecture** with a Python FastAPI backend and React frontend:

```
┌─────────────────────────────────────────────────────────────┐
│                     HIPS System Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │             Frontend (React + TypeScript)            │  │
│  │  - Dashboard, Alerts, Logs, Rules, Monitoring, etc.  │  │
│  │  - Real-time updates via WebSocket                   │  │
│  │  - Built with Vite, TailwindCSS, Recharts           │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↕ (HTTP/WebSocket)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Backend (Python FastAPI + Uvicorn)         │  │
│  │                                                       │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │           API Layer (FastAPI)               │   │  │
│  │  │  - /api/v1/alerts, /api/v1/logs, /ws/*     │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  │                     ↑                               │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │  Rule Engine & Event Processing             │   │  │
│  │  │  - Loads YAML rules                         │   │  │
│  │  │  - Matches events against conditions        │   │  │
│  │  │  - Triggers alerts and actions              │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  │                     ↑                               │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │           Monitoring Layer                  │   │  │
│  │  │  - ProcessMonitor (psutil)                 │   │  │
│  │  │  - FilesystemMonitor (watchdog)             │   │  │
│  │  │  - RegistryMonitor (Windows)                │   │  │
│  │  │  - NetworkMonitor                           │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  │                     ↑                               │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │  Event Bus & Activity Logger                │   │  │
│  │  │  - Central pub/sub for events               │   │  │
│  │  │  - Persists events to database              │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         SQLite Database (hips_data.db)              │  │
│  │  - alerts table                                      │  │
│  │  - activity_logs table                              │  │
│  │  - blocked_actions table                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
- **Python 3.9+**
- **FastAPI** - Web framework for REST API
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and settings management
- **psutil** - Process monitoring
- **watchdog** - Filesystem monitoring
- **pyyaml** - YAML rule parsing
- **websockets** - Real-time bidirectional communication
- **SQLite** - Lightweight embedded database

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **TailwindCSS** - Utility-first CSS framework
- **Radix UI** - Accessible UI components
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **TanStack React Query** - Server state management
- **Zustand** - Client state management
- **date-fns** - Date utilities
- **Lucide React** - Icon library

---

## Features

### Core Monitoring
- ✅ **Process Monitoring** - Detects process creation, termination, and privilege escalation
- ✅ **Filesystem Monitoring** - Tracks file creation, modification, deletion, and rapid changes (ransomware detection)
- ✅ **Registry Monitoring** - Windows registry key and value changes
- ✅ **Network Monitoring** - Outbound/inbound connections on suspicious ports

### Detection & Prevention
- ✅ **YAML Rule Engine** - 25+ pre-configured detection rules
- ✅ **Pattern Matching** - Regular expressions, string matching, numeric comparisons
- ✅ **Frequency-based Detection** - Identifies rapid events (ransomware, brute force)
- ✅ **Process Blocking** - Terminates malicious processes
- ✅ **Action Framework** - Alert, block, log, notify via webhooks

### Alert Management
- ✅ **Severity Levels** - Low, Medium, High, Critical
- ✅ **Alert Status** - New, Acknowledged, Resolved
- ✅ **Rate Limiting** - Configurable alerts per hour per rule
- ✅ **Retention Policies** - Auto-cleanup of old alerts (configurable days)

### Dashboard & Visualization
- ✅ **Real-time Dashboard** - Live event metrics, event type distribution
- ✅ **Alerts Page** - View, filter, acknowledge, resolve, delete alerts
- ✅ **Logs Page** - Complete activity history with advanced filtering
- ✅ **Rules Management** - Create, edit, disable, download, upload rules
- ✅ **Monitoring Status** - Active monitors and capabilities
- ✅ **Reports** - Generate PDF reports of security activities
- ✅ **Settings** - Configure monitoring intervals, watched paths, excluded processes

### Rules Included
Pre-configured rules detect:
- 🚨 Ransomware (rapid file changes, suspicious extensions)
- 🚨 Cryptocurrency miners
- 🚨 Lateral movement attempts
- 🚨 Windows Defender disabling
- 🚨 UAC bypass techniques
- 🚨 Registry persistence (AppInit DLL, Run keys, Winlogon)
- 🚨 LSA modification attempts
- 🚨 Credential dumping
- 🚨 LOLBAS abuse
- 🚨 PowerShell exploitation
- 🚨 Shadow copy deletion
- 🚨 Event log clearing
- 🚨 Firewall disabling
- 🚨 Scheduled task persistence
- 🚨 Office spawning shell
- 🚨 Netcat usage
- 🚨 Reverse shell detection
- 🚨 Port scanning
- 🚨 Data exfiltration (curl/wget)
- 🚨 Encoded PowerShell commands

---

## Installation & Setup

### Prerequisites

- **Python 3.9+** for backend
- **Node.js 18+** and **npm** for frontend
- **Windows** or **Linux** operating system

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -m hips_service.main
   ```

   Expected output:
   ```
   ✓ All components started successfully
   ✓ API server starting on 0.0.0.0:8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   Expected output:
   ```
   ➜  Local:   http://localhost:5173/
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

### Quick Start (5 minutes)

**Terminal 1 - Backend:**
```bash
cd backend
python -m hips_service.main
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Browser:**
Open http://localhost:5173

---

## Configuration

### Main Configuration File: `config/hips_config.yaml`

```yaml
api:
  host: 0.0.0.0
  port: 8000
  log_level: info
  reload: false

database:
  path: ./hips_data.db
  echo: false
  pool_size: 5

process_monitoring:
  enabled: true
  interval_seconds: 6
  max_events_per_batch: 100
  track_children: true
  monitor_privilege_escalation: true

file_monitoring:
  enabled: true
  interval_seconds: 10
  max_events_per_batch: 100
  watched_paths:
    - C:\Users
    - C:\Windows\System32
    - C:\Windows\SysWOW64
    - C:\Program Files
    - C:\Program Files (x86)
  excluded_extensions:
    - .tmp
    - .swp
    - .log
    - .db-journal
    - .db-shm
    - .db-wal
    - .pyc
  detect_rapid_changes: false
  rapid_change_threshold: 30
  rapid_change_window_seconds: 60

network_monitoring:
  enabled: true
  interval_seconds: 5
  max_events_per_batch: 100
  monitor_outbound: true
  monitor_inbound: false
  suspicious_ports:
    - 4444, 5555, 6666, 7777, 8888, 9999
    - 1337, 31337, 12345, 54321

registry_monitoring:
  enabled: true

rules_directory: ./rules

log_retention_days: 30
```

### Runtime Settings: `hips_settings.json`

Settings that can be modified through the UI:
```json
{
  "monitoring": {
    "process_interval": 6,
    "filesystem_interval": 10,
    "network_interval": 5,
    "watched_paths": [],
    "excluded_processes": []
  },
  "alerts": {
    "max_per_hour": 100,
    "retention_days": 30,
    "email_notifications": true,
    "webhook_url": "https://webhook.site/..."
  },
  "database": {
    "retention_days": 90,
    "auto_cleanup": true,
    "max_size_mb": 500
  },
  "logging": {
    "level": "INFO",
    "max_file_size_mb": 10,
    "backup_count": 5
  }
}
```

### Environment Variables

- `HIPS_CONFIG` - Path to configuration file (default: `./config/hips_config.yaml`)
- `HIPS_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `HIPS_CORS_ORIGINS` - Comma-separated CORS origins for production

---

## Usage

### Web Dashboard Access

**Local Access:**
- http://localhost:5173

**Default Behavior:**
- Backend listens on `0.0.0.0:8000` (all interfaces)
- Frontend connects to backend via Vite proxy at `/api` and `/ws`

### Navigation

1. **Dashboard** - Overview of system status, recent alerts, event distribution
2. **Alerts** - View, filter, acknowledge, and resolve security alerts
3. **Logs** - Complete activity history for forensic analysis
4. **Rules** - Create, edit, enable/disable detection rules
5. **Monitoring** - View active monitors and their capabilities
6. **Reports** - Generate and download PDF security reports
7. **Settings** - Configure monitoring intervals, paths, processes, and alert thresholds

### Common Tasks

#### View Active Alerts
1. Click **Alerts** in sidebar
2. Filter by severity, date range, or status
3. Click alert to view details
4. Acknowledge or resolve

#### Create Custom Rule
1. Click **Rules** in sidebar
2. Click **Create Rule** button
3. Fill in rule details:
   - Rule ID, Name, Description
   - Severity (low/medium/high/critical)
   - Conditions (event type, field patterns)
   - Actions (alert, block_process, notify)
4. Click **Create**

#### Export Data
1. Click **Logs** or **Reports**
2. Use filter/search
3. Click **Download** to export data

---

## Rules System

### Rule Structure

All rules are YAML files in the `backend/rules/` directory:

```yaml
rule:
  id: "unique-rule-id"
  name: "Human Readable Rule Name"
  description: "What this rule detects and why"
  enabled: true
  severity: "critical"           # low, medium, high, critical
  category: "defense_evasion"    # threat category
  
  conditions:
    event_type: "process_create" # Type of event to match
    platform:                     # Platforms to apply to
      - "windows"
      - "linux"
    
    # Match conditions
    any:  # Match if ANY condition is true
      - field: "process_name"
        operator: "in"
        value:
          - "malicious.exe"
          - "bad.exe"
      
      - field: "process_cmdline"
        operator: "regex"
        value: "(?i)malicious.*command"
      
      - field: "file_path"
        operator: "contains"
        value: "/tmp/"
    
    all:  # Match if ALL conditions are true
      - field: "process_name"
        operator: "contains"
        value: "powershell"
      
      - field: "process_cmdline"
        operator: "regex"
        value: "(?i)encoded"
    
    # Frequency-based detection
    frequency:
      count: 10
      timeframe: 60s  # Within 60 seconds
  
  actions:
    - type: "alert"
      priority: "critical"
      message: "Alert message with {field_name} interpolation"
    
    - type: "block_process"
      target: "process_pid"
    
    - type: "log"
    
    - type: "notify"
      message: "Message sent to webhook_url from settings"
  
  metadata:
    author: "Security Team"
    references:
      - "https://attack.mitre.org/..."
    tags:
      - "malware"
      - "lateral-movement"
```

### Rule Field Operators

- **in** - Field is in a list
- **contains** - Field contains a substring (case-sensitive)
- **regex** - Field matches a regular expression
- **equals** - Field equals a value
- **gt** / **lt** / **gte** / **lte** - Numeric comparisons

### Event Types

- `process_create` - Process creation
- `process_terminate` - Process termination
- `file_created` - File creation
- `file_modified` - File modification
- `file_deleted` - File deletion
- `network_connect` - Network connection
- `registry_set` - Registry key set/modified
- `registry_delete` - Registry key deleted

### Example Rules

See `backend/rules/` for 25+ pre-configured examples:
- `ransomware-rapid-file-changes.yaml`
- `windows-defender-disable.yaml`
- `crypto-miner-detection.yaml`
- `reverse-shell-detection.yaml`
- `windows-uac-bypass.yaml`

---

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Alerts
- `GET /alerts` - Get alerts with filters
- `POST /alerts/{alert_id}/acknowledge` - Acknowledge alert
- `POST /alerts/{alert_id}/resolve` - Resolve alert
- `DELETE /alerts/{alert_id}` - Delete alert
- `GET /alerts/blocked-actions` - Get blocked actions

#### Logs
- `GET /logs` - Get activity logs with filters
- `GET /logs/{log_id}` - Get specific log entry

#### Rules
- `GET /rules` - Get all rules
- `POST /rules` - Create new rule
- `GET /rules/{rule_id}` - Get specific rule
- `PUT /rules/{rule_id}` - Update rule
- `DELETE /rules/{rule_id}` - Delete rule
- `POST /rules/{rule_id}/toggle` - Enable/disable rule
- `POST /rules/reload` - Reload all rules

#### Metrics
- `GET /metrics` - Get system metrics
- `GET /metrics/events` - Get event count by type
- `GET /metrics/alerts` - Get alert count by severity

#### System
- `GET /system/status` - System health and monitor status
- `GET /system/capabilities` - Monitoring capabilities

#### Monitoring
- `GET /monitoring/monitors` - List active monitors
- `PUT /monitoring/monitors/{monitor_name}` - Update monitor settings

#### Settings
- `GET /settings` - Get current settings
- `POST /settings` - Update settings
- `POST /settings/reset` - Reset to defaults
- `POST /settings/cleanup` - Cleanup old database records
- `GET /settings/db-info` - Database statistics

#### WebSocket
- `WS /ws` - Real-time event stream
  - Emits: `{"type": "activity", "data": {...}}`
  - Emits: `{"type": "alert", "data": {...}}`

---

## Database Schema

### alerts table
```sql
CREATE TABLE alerts (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME NOT NULL,
  rule_id VARCHAR(100),
  rule_name VARCHAR(200),
  severity VARCHAR(20),           -- low, medium, high, critical
  category VARCHAR(50),
  message TEXT,
  event_data TEXT,                -- JSON
  status VARCHAR(20),             -- new, acknowledged, resolved
  acknowledged_at DATETIME,
  resolved_at DATETIME,
  platform VARCHAR(20)
);
```

### activity_logs table
```sql
CREATE TABLE activity_logs (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME NOT NULL,
  event_type VARCHAR(50),         -- process_create, file_modify, etc.
  platform VARCHAR(20),
  severity VARCHAR(20),
  
  -- Process details
  process_name VARCHAR(255),
  process_pid INTEGER,
  process_path TEXT,
  process_cmdline TEXT,
  parent_pid INTEGER,
  parent_name VARCHAR(255),
  
  -- File details
  file_path TEXT,
  file_operation VARCHAR(50),
  file_hash VARCHAR(64),          -- SHA-256
  
  -- Network details
  src_ip VARCHAR(45),
  src_port INTEGER,
  dst_ip VARCHAR(45),
  dst_port INTEGER,
  protocol VARCHAR(10),
  
  -- Registry details (Windows)
  registry_key TEXT,
  registry_operation VARCHAR(50),
  registry_value TEXT,
  
  -- Additional
  user VARCHAR(100),
  extra_data TEXT                 -- JSON
);
```

### blocked_actions table
```sql
CREATE TABLE blocked_actions (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME NOT NULL,
  rule_id VARCHAR(100),
  action_type VARCHAR(50),        -- process_blocked, connection_blocked
  target TEXT,
  reason TEXT
);
```

---

## Monitoring Components

### ProcessMonitor
- **Capability:** Detects process creation, termination, privilege escalation
- **Method:** psutil process iteration
- **Interval:** 6 seconds (configurable)
- **Events:** process_create, process_terminate
- **Excluded Processes:** Configurable in settings (System, Registry, smss.exe by default)

### FilesystemMonitor
- **Capability:** Detects file creation, modification, deletion
- **Method:** watchdog file system events
- **Interval:** 10 seconds (configurable)
- **Events:** file_created, file_modified, file_deleted
- **Rapid Change Detection:** Identifies ransomware patterns (30+ files in 60s)
- **Suspicious Extensions:** .encrypted, .locked, .crypto, .wannacry, etc.
- **Excluded Extensions:** .tmp, .swp, .log, .pyc, etc.

### RegistryMonitor (Windows Only)
- **Capability:** Detects registry key and value changes
- **Method:** Windows Registry API monitoring
- **Events:** registry_set, registry_delete
- **Monitored Keys:** HKLM\SOFTWARE, HKCU\SOFTWARE, etc.

### NetworkMonitor
- **Capability:** Detects network connections
- **Method:** psutil network connections
- **Suspicious Ports:** 4444, 5555, 6666, 7777, 8888, 9999, 1337, 31337, etc.
- **Tracked Connections:** Destination IP, port, protocol

---

## Frontend Pages

### Dashboard (`/`)
- System status overview
- Real-time event count and alert distribution
- Recent alerts list (5 most recent)
- Recent activity logs (10 most recent)
- Event type statistics pie chart
- Live event and alert timeline (30-second rolling window)

### Alerts (`/alerts`)
- Filter by severity, date range, status
- Search alerts by rule name or message
- Acknowledge/resolve/delete individual alerts
- Bulk actions on selected alerts
- View blocked actions and their reasons
- Detailed alert modal with full event data

### Logs (`/logs`)
- Complete activity history
- Filter by event type, process name, file path
- Date range and severity filters
- Real-time log updates
- Export logs functionality
- Search and pagination

### Rules (`/rules`)
- View all loaded detection rules
- Create new rules with JSON editor
- Edit existing rules
- Enable/disable rules
- Delete rules
- Download/upload rule YAML files
- Toggle rule status (enable/disable)
- Reload rules from disk

### Monitoring (`/monitoring`)
- List active monitors (Process, Filesystem, Registry, Network)
- Display monitor capabilities
- Show current monitoring configuration
- Monitor status indicators
- Runtime configuration updates

### Reports (`/reports`)
- Generate PDF security reports
- Filter data by date range and severity
- Report templates with statistics
- Export formatted reports

### Settings (`/settings`)
- Configure monitoring intervals (process, file, network)
- Set watched paths for filesystem monitoring
- Configure excluded processes
- Alert rate limiting (max alerts per hour per rule)
- Database retention policies
- Auto-cleanup settings
- Database backup and download
- System health information
- Database statistics

---

## Project Structure

```
HIPS/
├── README.md                          # This file
├── QUICK_START.md                     # Quick start guide
├── USER_GUIDE.md                      # User guide
├── hips_settings.json                 # Runtime settings
│
├── backend/                           # Python FastAPI backend
│   ├── requirements.txt               # Python dependencies
│   ├── hips_service/
│   │   ├── __init__.py
│   │   ├── main.py                    # Entry point
│   │   ├── api/
│   │   │   ├── app.py                 # FastAPI app factory
│   │   │   └── routes/
│   │   │       ├── alerts.py
│   │   │       ├── logs.py
│   │   │       ├── rules.py
│   │   │       ├── metrics.py
│   │   │       ├── system.py
│   │   │       ├── websocket.py
│   │   │       ├── monitoring.py
│   │   │       ├── settings.py
│   │   │       ├── reports.py
│   │   │       └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py              # Configuration management
│   │   │   ├── event_bus.py           # Event pub/sub
│   │   │   ├── activity_logger.py     # Event logging to DB
│   │   │   ├── platform_detector.py   # OS detection
│   │   │   └── __init__.py
│   │   ├── database/
│   │   │   ├── models.py              # SQLAlchemy models
│   │   │   └── __init__.py
│   │   ├── monitors/
│   │   │   ├── base_monitor.py        # Abstract base class
│   │   │   ├── process_monitor.py     # Process monitoring
│   │   │   ├── filesystem_monitor.py  # Filesystem monitoring
│   │   │   ├── registry_monitor.py    # Windows registry monitoring
│   │   │   ├── platform/
│   │   │   └── __init__.py
│   │   ├── rules/
│   │   │   ├── engine.py              # Rule matching engine
│   │   │   ├── parser.py              # YAML parser
│   │   │   ├── matcher.py             # Pattern matching logic
│   │   │   ├── schema.py              # Rule data models
│   │   │   └── __init__.py
│   │   ├── service/
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── time.py                # Timezone utilities
│   │   │   └── __init__.py
│   │   └── assets/
│   ├── config/
│   │   └── hips_config.yaml           # Main configuration
│   └── rules/                         # YAML detection rules
│       ├── ransomware-rapid-file-changes.yaml
│       ├── windows-defender-disable.yaml
│       ├── crypto-miner-detection.yaml
│       ├── registry-appinit-dll.yaml
│       └── ... (25+ rules)
│
├── frontend/                          # React + TypeScript frontend
│   ├── package.json                   # Node dependencies
│   ├── tsconfig.json                  # TypeScript config
│   ├── vite.config.ts                 # Vite configuration
│   ├── tailwind.config.js             # TailwindCSS config
│   ├── index.html                     # HTML entry point
│   ├── src/
│   │   ├── main.tsx                   # React entry point
│   │   ├── App.tsx                    # Main app component
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Alerts.tsx
│   │   │   ├── Logs.tsx
│   │   │   ├── Rules.tsx
│   │   │   ├── Monitoring.tsx
│   │   │   ├── Reports.tsx
│   │   │   └── Settings.tsx
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   └── MainLayout.tsx
│   │   │   └── ui/                    # Radix UI wrapper components
│   │   │       ├── card.tsx
│   │   │       ├── button.tsx
│   │   │       ├── badge.tsx
│   │   │       ├── dialog.tsx
│   │   │       ├── table.tsx
│   │   │       └── ... (more UI components)
│   │   ├── services/
│   │   │   ├── api.ts                 # Axios instance
│   │   │   ├── alertsService.ts       # Alerts API calls
│   │   │   ├── logsService.ts         # Logs API calls
│   │   │   ├── rulesService.ts        # Rules API calls
│   │   │   ├── dashboardService.ts    # Dashboard metrics
│   │   │   ├── settingsService.ts     # Settings API calls
│   │   │   └── websocketService.ts    # WebSocket connection
│   │   ├── hooks/
│   │   │   └── useDarkMode.ts         # Dark mode toggle
│   │   ├── types/
│   │   │   └── ... TypeScript interfaces
│   │   ├── utils/
│   │   │   └── ... Helper functions
│   │   └── styles/
│   │       ├── globals.css            # TailwindCSS imports
│   │       └── ... (component styles)
│   └── postcss.config.js              # PostCSS for TailwindCSS
```

---

## Development

### Backend Development

**Start Backend with Auto-Reload:**
```bash
cd backend
python -m hips_service.main
```

**View Logs:**
```bash
tail -f hips.log
```

**Test Rule Engine:**
```python
from hips_service.rules.parser import RuleParser
rule = RuleParser.parse_file('backend/rules/crypto-miner-detection.yaml')
print(rule)
```

### Frontend Development

**Start Dev Server:**
```bash
cd frontend
npm run dev
```

**Build for Production:**
```bash
npm run build
```

**TypeScript Checking:**
```bash
npm run build  # Includes `tsc` check
```

### Testing Rules

1. Create test event:
   ```python
   from hips_service.core.event_bus import MonitorEvent, EventBus
   from datetime import datetime
   
   event = MonitorEvent(
       timestamp=datetime.now(),
       event_type="process_create",
       platform="windows",
       severity="high",
       data={
           "process_name": "xmrig.exe",
           "process_pid": 1234,
           "process_cmdline": "xmrig.exe -o pool.minexmr.com"
       }
   )
   ```

2. Match against rule:
   ```python
   from hips_service.rules.matcher import RuleMatcher
   matcher = RuleMatcher()
   result = matcher.match(event, rule)
   print(f"Matched: {result}")
   ```

### Database Inspection

**View Database:**
```bash
sqlite3 hips_data.db
```

**Sample Queries:**
```sql
-- Count alerts by severity
SELECT severity, COUNT(*) FROM alerts GROUP BY severity;

-- Recent alerts
SELECT id, rule_name, severity, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 10;

-- Activity by event type
SELECT event_type, COUNT(*) FROM activity_logs GROUP BY event_type;

-- Alert timeline
SELECT strftime('%Y-%m-%d %H:%00:00', timestamp) as hour, COUNT(*) 
FROM alerts GROUP BY hour ORDER BY hour DESC LIMIT 24;
```

### Troubleshooting

**Backend won't start:**
```bash
# Check port 8000 not in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Check Python version
python3 --version  # Needs 3.9+
```

**Frontend won't start:**
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

**No events appearing:**
```bash
# Check backend is running
curl http://localhost:8000/api/v1/system/status

# Check logs
tail -f backend/hips.log

# Verify monitors are enabled in config
grep enabled: config/hips_config.yaml
```

**WebSocket connection failing:**
```bash
# Check WebSocket proxy in vite.config.ts
# Ensure backend is running with WebSocket support
# Check browser console for error details
```

---

## Contributing

### Adding New Rules

1. Create YAML file in `backend/rules/`:
   ```yaml
   rule:
     id: "my-detection-rule"
     name: "My Detection"
     # ... rest of rule
   ```

2. Restart backend - rules are auto-loaded from directory

3. Verify rule appears in Rules page

### Adding New Features

1. **Backend Feature:**
   - Add route in `backend/hips_service/api/routes/`
   - Update API documentation above
   - Restart backend

2. **Frontend Feature:**
   - Add page in `frontend/src/pages/`
   - Add service in `frontend/src/services/`
   - Add route in `src/App.tsx`
   - Run `npm run dev`

---

## License

FSKTM Data Centre Security Team

---

## Support

For issues or questions:
1. Check logs: `tail -f backend/hips.log`
2. Review configuration: `config/hips_config.yaml`
3. Test rule matching with sample events
4. Check database for error records
