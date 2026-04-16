# Azure Arc Workbooks

This repository now includes two Azure Monitor Workbooks:

- `AzureArc-Comprehensive.workbook` - unified dashboard for **Azure Arc-enabled Windows Servers, Linux Servers, and SQL Server** instances.
- `AzureArc-Metrics-DeepDive.workbook` - metrics-focused operational dashboard with broad Arc telemetry coverage (connectivity, agent health, extensions, SQL/ESU, and governance).

The comprehensive workbook consolidates information from 7 community workbooks/dashboards into one broad view.

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

## Tab Structure (11 tabs, 88+ queries)

| Tab | Description |
|-----|-------------|
| **Overview** | 10 KPI tiles (server counts, SQL instances, EOL versions), OS distribution charts, servers-per-subscription grid |
| **Windows Servers** | Server status filter, cores-by-OS chart, full inventory grid with ESU status, hardware details |
| **Linux Servers** | Server status filter, cores-by-OS chart, full inventory grid with hardware details |
| **Extensions Windows** | 4 auto-discovered extension selectors, pie charts per extension status, detail grid with version/status icons |
| **Extensions Linux** | Same as Windows extensions but filtered for Linux |
| **ESU Tracking** | Win 2012/SQL 2012/SQL 2014 ESU charts, % assigned by subscription, Standard vs Datacenter, grids by sub/RG |
| **Windows Arc Benefits** | 9 sub-tabs: Overview, Update Manager, Defender, Inventory, Guest Config, Monitoring, Tagging, WAC, Hotpatching — each with pie chart + server detail grid |
| **SQL Servers & Databases** | 5 sub-tabs: SQL Overview, Databases (compat/recovery/backup), Defender for SQL, BPA status, Performance monitoring |
| **SQL Assessment** | Log Analytics workspace selector, issues by server/database/severity, drill-down detail grid (requires SqlAssessment_CL) |
| **Tags** | Distribution charts by Application, DataCenter, BusinessUnit, Location, Environment tags — all servers + SQL hosts |
| **Log Analytics** | Gap analysis — machines in Log Analytics NOT in Arc/Azure VMs (candidates for Arc onboarding) |

## How to Deploy

1. Go to **Azure Portal → Monitor → Workbooks → New**
2. Click the **Advanced Editor** button (`</>` icon)
3. Delete all content, paste the entire contents of one workbook file:
	- `AzureArc-Comprehensive.workbook` for the all-in-one estate dashboard
	- `AzureArc-Metrics-DeepDive.workbook` for deep metrics and operational views
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

---

## Disclaimer

This is a **personal repository** maintained independently. It is **not** an official product or deliverable of any vendor. It is provided **"as-is"** without warranty of any kind, express or implied. No vendor endorses, supports, or assumes responsibility for this workbook or its contents.

Use at your own risk. The authors and contributors accept no liability for any damage, data loss, or costs arising from the use of this workbook. Always validate queries and configurations in a non-production environment before deploying to production.

All source workbooks and dashboards referenced above are subject to their own respective licenses and terms.
