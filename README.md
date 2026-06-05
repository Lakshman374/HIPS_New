# CHIPS - Host Intrusion Prevention System

A comprehensive, cross-platform security monitoring and intrusion prevention system designed for FSKTM Data Centre with real-time threat detection, rule-based event matching, and a modern web-based dashboard.

---

## ðŸ“‹ Table of Contents

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

CHIPS (Intrusion Prevention System) is a real-time security monitoring solution that:

- **Monitors** system activities across process execution, filesystem operations, network connections, and Windows registry changes
- **Detects** threats using YAML-based detection rules
- **Alerts** on suspicious activities with severity classifications (low, medium, high, critical)
- **Blocks** malicious processes and connections based on configured rules
- **Logs** all events to a local SQLite database for forensic analysis
- **Visualizes** security data through an interactive React-based dashboard with real-time WebSocket updates

---

## Architecture

CHIPS follows a **client-server architecture** with a Python FastAPI backend and React frontend:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                     CHIPS System Architecture                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                               â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚             Frontend (React + TypeScript)            â”‚  â”‚
â”‚  â”‚  - Dashboard, Alerts, Logs, Rules, Monitoring, etc.  â”‚  â”‚
â”‚  â”‚  - Real-time updates via WebSocket                   â”‚  â”‚
â”‚  â”‚  - Built with Vite, TailwindCSS, Recharts           â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚                           â†• (HTTP/WebSocket)                â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚          Backend (Python FastAPI + Uvicorn)         â”‚  â”‚
â”‚  â”‚                                                       â”‚  â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚  â”‚
â”‚  â”‚  â”‚           API Layer (FastAPI)               â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - /api/v1/alerts, /api/v1/logs, /ws/*     â”‚   â”‚  â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚  â”‚
â”‚  â”‚                     â†‘                               â”‚  â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚  â”‚
â”‚  â”‚  â”‚  Rule Engine & Event Processing             â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - Loads YAML rules                         â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - Matches events against conditions        â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - Triggers alerts and actions              â”‚   â”‚  â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚  â”‚
â”‚  â”‚                     â†‘                               â”‚  â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚  â”‚
â”‚  â”‚  â”‚           Monitoring Layer                  â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - ProcessMonitor (psutil)                 â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - FilesystemMonitor (watchdog)             â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - RegistryMonitor (Windows)                â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - NetworkMonitor                           â”‚   â”‚  â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚  â”‚
â”‚  â”‚                     â†‘                               â”‚  â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚  â”‚
â”‚  â”‚  â”‚  Event Bus & Activity Logger                â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - Central pub/sub for events               â”‚   â”‚  â”‚
â”‚  â”‚  â”‚  - Persists events to database              â”‚   â”‚  â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚  â”‚
â”‚  â”‚                                                      â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚                           â†“                                  â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚         SQLite Database (hips_data.db)              â”‚  â”‚
â”‚  â”‚  - alerts table                                      â”‚  â”‚
â”‚  â”‚  - activity_logs table                              â”‚  â”‚
â”‚  â”‚  - blocked_actions table                            â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚                                                               â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
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
- âœ… **Process Monitoring** - Detects process creation, termination, and privilege escalation
- âœ… **Filesystem Monitoring** - Tracks file creation, modification, deletion, and rapid changes (ransomware detection)
- âœ… **Registry Monitoring** - Windows registry key and value changes
- âœ… **Network Monitoring** - Outbound/inbound connections on suspicious ports

### Detection & Prevention
- âœ… **YAML Rule Engine** - 25+ pre-configured detection rules
- âœ… **Pattern Matching** - Regular expressions, string matching, numeric comparisons
- âœ… **Frequency-based Detection** - Identifies rapid events (ransomware, brute force)
- âœ… **Process Blocking** - Terminates malicious processes
- âœ… **Action Framework** - Alert, block, log, notify via webhooks

### Alert Management
- âœ… **Severity Levels** - Low, Medium, High, Critical
- âœ… **Alert Status** - New, Acknowledged, Resolved
- âœ… **Rate Limiting** - Configurable alerts per hour per rule
- âœ… **Retention Policies** - Auto-cleanup of old alerts (configurable days)

### Dashboard & Visualization
- âœ… **Real-time Dashboard** - Live event metrics, event type distribution
- âœ… **Alerts Page** - View, filter, acknowledge, resolve, delete alerts
- âœ… **Logs Page** - Complete activity history with advanced filtering
- âœ… **Rules Management** - Create, edit, disable, download, upload rules
- âœ… **Monitoring Status** - Active monitors and capabilities
- âœ… **Reports** - Generate PDF reports of security activities
- âœ… **Settings** - Configure monitoring intervals, watched paths, excluded processes

### Rules Included
Pre-configured rules detect:
- ðŸš¨ Ransomware (rapid file changes, suspicious extensions)
- ðŸš¨ Cryptocurrency miners
- ðŸš¨ Lateral movement attempts
- ðŸš¨ Windows Defender disabling
- ðŸš¨ UAC bypass techniques
- ðŸš¨ Registry persistence (AppInit DLL, Run keys, Winlogon)
- ðŸš¨ LSA modification attempts
- ðŸš¨ Credential dumping
- ðŸš¨ LOLBAS abuse
- ðŸš¨ PowerShell exploitation
- ðŸš¨ Shadow copy deletion
- ðŸš¨ Event log clearing
- ðŸš¨ Firewall disabling
- ðŸš¨ Scheduled task persistence
- ðŸš¨ Office spawning shell
- ðŸš¨ Netcat usage
- ðŸš¨ Reverse shell detection
- ðŸš¨ Port scanning
- ðŸš¨ Data exfiltration (curl/wget)
- ðŸš¨ Encoded PowerShell commands

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
   âœ“ All components started successfully
   âœ“ API server starting on 0.0.0.0:8000
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
   âžœ  Local:   http://localhost:5173/
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

### Main Configuration File: `config/CHIPS_CONFIG.yaml`

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

- `CHIPS_CONFIG` - Path to configuration file (default: `./config/CHIPS_CONFIG.yaml`)
- `CHIPS_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `CHIPS_CORS_ORIGINS` - Comma-separated CORS origins for production

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
CHIPS/
â”œâ”€â”€ README.md                          # This file
â”œâ”€â”€ QUICK_START.md                     # Quick start guide
â”œâ”€â”€ USER_GUIDE.md                      # User guide
â”œâ”€â”€ hips_settings.json                 # Runtime settings
â”‚
â”œâ”€â”€ backend/                           # Python FastAPI backend
â”‚   â”œâ”€â”€ requirements.txt               # Python dependencies
â”‚   â”œâ”€â”€ hips_service/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ main.py                    # Entry point
â”‚   â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”‚   â”œâ”€â”€ app.py                 # FastAPI app factory
â”‚   â”‚   â”‚   â””â”€â”€ routes/
â”‚   â”‚   â”‚       â”œâ”€â”€ alerts.py
â”‚   â”‚   â”‚       â”œâ”€â”€ logs.py
â”‚   â”‚   â”‚       â”œâ”€â”€ rules.py
â”‚   â”‚   â”‚       â”œâ”€â”€ metrics.py
â”‚   â”‚   â”‚       â”œâ”€â”€ system.py
â”‚   â”‚   â”‚       â”œâ”€â”€ websocket.py
â”‚   â”‚   â”‚       â”œâ”€â”€ monitoring.py
â”‚   â”‚   â”‚       â”œâ”€â”€ settings.py
â”‚   â”‚   â”‚       â”œâ”€â”€ reports.py
â”‚   â”‚   â”‚       â””â”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ core/
â”‚   â”‚   â”‚   â”œâ”€â”€ config.py              # Configuration management
â”‚   â”‚   â”‚   â”œâ”€â”€ event_bus.py           # Event pub/sub
â”‚   â”‚   â”‚   â”œâ”€â”€ activity_logger.py     # Event logging to DB
â”‚   â”‚   â”‚   â”œâ”€â”€ platform_detector.py   # OS detection
â”‚   â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ database/
â”‚   â”‚   â”‚   â”œâ”€â”€ models.py              # SQLAlchemy models
â”‚   â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ monitors/
â”‚   â”‚   â”‚   â”œâ”€â”€ base_monitor.py        # Abstract base class
â”‚   â”‚   â”‚   â”œâ”€â”€ process_monitor.py     # Process monitoring
â”‚   â”‚   â”‚   â”œâ”€â”€ filesystem_monitor.py  # Filesystem monitoring
â”‚   â”‚   â”‚   â”œâ”€â”€ registry_monitor.py    # Windows registry monitoring
â”‚   â”‚   â”‚   â”œâ”€â”€ platform/
â”‚   â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ rules/
â”‚   â”‚   â”‚   â”œâ”€â”€ engine.py              # Rule matching engine
â”‚   â”‚   â”‚   â”œâ”€â”€ parser.py              # YAML parser
â”‚   â”‚   â”‚   â”œâ”€â”€ matcher.py             # Pattern matching logic
â”‚   â”‚   â”‚   â”œâ”€â”€ schema.py              # Rule data models
â”‚   â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ service/
â”‚   â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ utils/
â”‚   â”‚   â”‚   â”œâ”€â”€ time.py                # Timezone utilities
â”‚   â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”‚   â””â”€â”€ assets/
â”‚   â”œâ”€â”€ config/
â”‚   â”‚   â””â”€â”€ CHIPS_CONFIG.yaml           # Main configuration
â”‚   â””â”€â”€ rules/                         # YAML detection rules
â”‚       â”œâ”€â”€ ransomware-rapid-file-changes.yaml
â”‚       â”œâ”€â”€ windows-defender-disable.yaml
â”‚       â”œâ”€â”€ crypto-miner-detection.yaml
â”‚       â”œâ”€â”€ registry-appinit-dll.yaml
â”‚       â””â”€â”€ ... (25+ rules)
â”‚
â”œâ”€â”€ frontend/                          # React + TypeScript frontend
â”‚   â”œâ”€â”€ package.json                   # Node dependencies
â”‚   â”œâ”€â”€ tsconfig.json                  # TypeScript config
â”‚   â”œâ”€â”€ vite.config.ts                 # Vite configuration
â”‚   â”œâ”€â”€ tailwind.config.js             # TailwindCSS config
â”‚   â”œâ”€â”€ index.html                     # HTML entry point
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”œâ”€â”€ main.tsx                   # React entry point
â”‚   â”‚   â”œâ”€â”€ App.tsx                    # Main app component
â”‚   â”‚   â”œâ”€â”€ pages/
â”‚   â”‚   â”‚   â”œâ”€â”€ Dashboard.tsx
â”‚   â”‚   â”‚   â”œâ”€â”€ Alerts.tsx
â”‚   â”‚   â”‚   â”œâ”€â”€ Logs.tsx
â”‚   â”‚   â”‚   â”œâ”€â”€ Rules.tsx
â”‚   â”‚   â”‚   â”œâ”€â”€ Monitoring.tsx
â”‚   â”‚   â”‚   â”œâ”€â”€ Reports.tsx
â”‚   â”‚   â”‚   â””â”€â”€ Settings.tsx
â”‚   â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â”‚   â”œâ”€â”€ layout/
â”‚   â”‚   â”‚   â”‚   â””â”€â”€ MainLayout.tsx
â”‚   â”‚   â”‚   â””â”€â”€ ui/                    # Radix UI wrapper components
â”‚   â”‚   â”‚       â”œâ”€â”€ card.tsx
â”‚   â”‚   â”‚       â”œâ”€â”€ button.tsx
â”‚   â”‚   â”‚       â”œâ”€â”€ badge.tsx
â”‚   â”‚   â”‚       â”œâ”€â”€ dialog.tsx
â”‚   â”‚   â”‚       â”œâ”€â”€ table.tsx
â”‚   â”‚   â”‚       â””â”€â”€ ... (more UI components)
â”‚   â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â”‚   â”œâ”€â”€ api.ts                 # Axios instance
â”‚   â”‚   â”‚   â”œâ”€â”€ alertsService.ts       # Alerts API calls
â”‚   â”‚   â”‚   â”œâ”€â”€ logsService.ts         # Logs API calls
â”‚   â”‚   â”‚   â”œâ”€â”€ rulesService.ts        # Rules API calls
â”‚   â”‚   â”‚   â”œâ”€â”€ dashboardService.ts    # Dashboard metrics
â”‚   â”‚   â”‚   â”œâ”€â”€ settingsService.ts     # Settings API calls
â”‚   â”‚   â”‚   â””â”€â”€ websocketService.ts    # WebSocket connection
â”‚   â”‚   â”œâ”€â”€ hooks/
â”‚   â”‚   â”‚   â””â”€â”€ useDarkMode.ts         # Dark mode toggle
â”‚   â”‚   â”œâ”€â”€ types/
â”‚   â”‚   â”‚   â””â”€â”€ ... TypeScript interfaces
â”‚   â”‚   â”œâ”€â”€ utils/
â”‚   â”‚   â”‚   â””â”€â”€ ... Helper functions
â”‚   â”‚   â””â”€â”€ styles/
â”‚   â”‚       â”œâ”€â”€ globals.css            # TailwindCSS imports
â”‚   â”‚       â””â”€â”€ ... (component styles)
â”‚   â””â”€â”€ postcss.config.js              # PostCSS for TailwindCSS
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
grep enabled: config/CHIPS_CONFIG.yaml
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
2. Review configuration: `config/CHIPS_CONFIG.yaml`
3. Test rule matching with sample events
4. Check database for error records

