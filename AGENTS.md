# Azure Arc Comprehensive Workbook

## What This Is

A single Azure Monitor Workbook (`.workbook` JSON file) that provides a unified dashboard for **Azure Arc-enabled Windows Servers, Linux Servers, and SQL Server** instances. It consolidates information from 7 community workbooks/dashboards into one comprehensive view with 11 tabs.

## Sources Combined

| Source | What It Contributed |
|--------|-------------------|
| [Azure Arc for Servers](https://github.com/microsoft/AzureMonitorCommunity/tree/master/Azure%20Services/Azure%20Arc/Workbooks/Azure%20Arc%20for%20Servers) | Base Arc server workbook structure, ESU information |
| [AzureArcServers&VMsExtensionsMonitor](https://github.com/microsoft/AzureMonitorCommunity/blob/master/Azure%20Services/Azure%20Arc/Workbooks/Azure%20Arc%20for%20Servers/AzureArcServers%26VMsExtensionsMonitor.workbook) | Extensions monitoring (Windows/Linux), auto-discovered extension dropdowns, Log Analytics gap analysis |
| [ArcBenefitsDashboard v2](https://github.com/wjpigott/ArcBenefitsDashboard) | Windows Arc benefits (10 capabilities), SQL Arc benefits (4 capabilities), cost analysis toggle, collapsible notes |
| [Arc - Estate Profile](https://github.com/microsoft/sql-server-samples/blob/master/samples/features/azure-arc/dashboard/Arc%20-%20Estate%20Profile.json) | Estate-wide KPI tiles, OS distribution charts, server counts by subscription/RG, tag distribution, core counts |
| [Arc - ESU Tracker](https://github.com/tps99/Arc-Azure-Portal-Dashboards/blob/main/Dashboards/Arc%20-%20ESU%20Tracker.json) | ESU assignment tracking for Win 2012, SQL 2012, SQL 2014; % assigned by subscription; edition breakdowns |
| [Azure Arc SQL Databases](https://github.com/microsoft/sql-server-samples/blob/master/samples/features/azure-arc/workbooks/Azure%20Arc%20Sql%20Databases.workbook) | SQL database inventory — compatibility level, recovery model, backup status |
| [Azure Arc SQL BPA](https://github.com/microsoft/sql-server-samples/blob/master/samples/features/azure-arc/workbooks/Azure%20Arc%20Sql%20Servers%20-%20Best%20Practices%20Assessment.workbook) | SQL Best Practices Assessment from Log Analytics (SqlAssessment_CL), severity drill-down |

## Tab Structure (13 tabs, 100+ queries)

| Tab | Description |
|-----|-------------|
| **Overview** | 10 KPI tiles (server counts, SQL instances, EOL versions), OS distribution charts, servers-per-subscription grid |
| **Windows Servers** | Server status filter, cores-by-OS chart, full inventory grid with ESU status, hardware details, manufacturer/model, domain, FQDN, license type, Software Assurance |
| **Linux Servers** | Server status filter, cores-by-OS chart, full inventory grid with hardware details, manufacturer/model, domain, FQDN |
| **Extensions Windows** | 4 auto-discovered extension selectors, pie charts per extension status, detail grid with version/status icons |
| **Extensions Linux** | Same as Windows extensions but filtered for Linux |
| **ESU Tracking** | Win 2012/SQL 2012/SQL 2014 ESU charts, % assigned by subscription, Standard vs Datacenter, grids by sub/RG |
| **Windows Arc Benefits** | 12 sub-tabs: Overview, Update Manager, Defender, Inventory, Guest Config, Monitoring, Tagging, WAC, Hotpatching, Change Tracking, Key Vault, Hybrid Workers — each with pie chart + server detail grid |
| **Linux Arc Benefits** | 7 sub-tabs: Overview, Update Manager, Defender, Guest Config, Monitoring, Tagging, SSH Access — each with pie chart + server detail grid |
| **SQL Servers & Databases** | 5 sub-tabs: SQL Overview (with licenseType/currentVersion), Databases (compat/recovery/backup), Defender for SQL, BPA status, Performance monitoring |
| **SQL Assessment** | Log Analytics workspace selector, issues by server/database/severity, drill-down detail grid (requires SqlAssessment_CL) |
| **Tags** | Distribution charts by Application, DataCenter, BusinessUnit, Location, Environment tags — all servers + SQL hosts |
| **Log Analytics** | Gap analysis — machines in Log Analytics NOT in Arc/Azure VMs (candidates for Arc onboarding) |
| **Agent Health** | Agent version distribution, disconnected servers, agent errors, service status, cloud provider distribution, license compliance summary |

## File Structure

```
arc_workbook/
├── AzureArc-Comprehensive.workbook   # Final combined workbook (import this)
├── combine.py                         # Script to rebuild from parts
├── AGENTS.md                          # This file
└── parts/                             # Individual tab sections
    ├── 00_parameters.json             # Global parameters + cost params
    ├── 01_tabs.json                   # Tab navigation
    ├── 02_overview.json               # Overview & Estate Profile
    ├── 03_windows_servers.json        # Windows Server Details
    ├── 04_linux_servers.json          # Linux Server Details
    ├── 05_extensions_windows.json     # Extensions Windows
    ├── 06_extensions_linux.json       # Extensions Linux
    ├── 07_esu_tracking.json           # ESU Tracking
    ├── 08_windows_benefits.json       # Windows Arc Benefits (12 sub-tabs)
    ├── 08b_linux_benefits.json        # Linux Arc Benefits (7 sub-tabs)
    ├── 09_sql_servers.json            # SQL Servers & Databases (5 sub-tabs)
    ├── 10_sql_assessment.json         # SQL BPA (Log Analytics)
    ├── 11_tags.json                   # Tag Distribution
    ├── 12_log_analytics.json          # Log Analytics Gap Analysis
    └── 13_agent_health.json           # Agent Health & Operational Visibility
```

## How to Deploy

1. Go to **Azure Portal → Monitor → Workbooks → New**
2. Click the **Advanced Editor** button (`</>` icon)
3. Delete all content, paste the entire contents of `AzureArc-Comprehensive.workbook`
4. Click **Apply** → **Save**

## How to Edit

Edit individual part files in `parts/`, then regenerate:

```bash
python3 combine.py
```

This merges all `parts/*.json` files (sorted by filename) into `AzureArc-Comprehensive.workbook`.

## Global Features

- **Subscription filter** — multi-select, default: all
- **Machine Type filter** — Arc Servers / Azure VMs / Both
- **Cost Analysis toggle** — off by default; enables 13 customizable cost parameters
- **Time Range** — for Log Analytics queries
- **Export to Excel** on all detail grids

## Query Types

- **Azure Resource Graph (81 queries)** — estate, extensions, ESU, benefits, SQL databases
- **Log Analytics (6 queries)** — SQL BPA (SqlAssessment_CL), Heartbeat gap analysis
- **Merge (1 query)** — Log Analytics gap analysis (left anti-join)

## Prerequisites

- **Reader** role on subscriptions to monitor
- For SQL tabs: SQL Server instances registered as `microsoft.azurearcdata/sqlserverinstances`
- For SQL Assessment tab: Log Analytics workspace with `SqlAssessment_CL` data
- For Defender for SQL tab: Security Reader role (queries `securityresources`)

## Known ARG Limitations

Azure Resource Graph does not support all Kusto/ADX functions. Avoid:
- `pack_array()`, `pack()` for building dynamic arrays/objects to unpack
- `mv-expand` + `evaluate bag_unpack()` for pivoting
- `countif()` can be unreliable — use `sum(iff(..., 1, 0))` instead

## Build History

- **v1.0** — Initial creation combining all 7 sources into 11 tabs with 88 queries
- **v2.0** — Added Linux Arc Benefits tab (7 sub-tabs), Agent Health tab (6 panels), 3 new Windows Arc Benefits sub-tabs (Change Tracking, Key Vault, Hybrid Workers), enriched inventory grids with manufacturer/model/domain/FQDN/license columns, enriched SQL grid with licenseType/currentVersion. Now 13 tabs, 100+ queries across 15 part files
- Split into 13 part files for maintainability
- Fixed ARG-incompatible KQL in Windows Arc Capabilities Summary (replaced `pack_array`/`mv-expand`/`bag_unpack` with `sum()` aggregation)
- Added server detail grid to WAC sub-tab
