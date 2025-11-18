# Storytelling Data → Frontend Component Mapping

## Data Sources
- Loader module: `data_sources/storytelling_loader.py`
- Assets: `data/outputs/nova_corrente/storytelling/`

## Component Wiring (React pseudo-code)

```tsx
// src/hooks/useStorytellingData.ts
import { useEffect, useState } from 'react';

export function useStorytellingData() {
  const [kpis, setKpis] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [timeseries, setTimeseries] = useState([]);

  useEffect(() => {
    fetch('/api/storytelling/kpis').then(r => r.json()).then(setKpis);
    fetch('/api/storytelling/alerts?status=critical').then(r => r.json()).then(setAlerts);
    fetch('/api/storytelling/timeseries?family=ABRASIVOS').then(r => r.json()).then(setTimeseries);
  }, []);

  return { kpis, alerts, timeseries };
}
```

```tsx
// Dashboards
<SummaryHero data={kpis} />
<ForecastHeatmap data={timeseries} />
<AlertCommandCenter alerts={alerts} />
```

## API Contract (FastAPI / Flask)
- `GET /api/storytelling/kpis` → `get_kpi_snapshot()`
- `GET /api/storytelling/alerts` → params: `status[]`, `familia`
- `GET /api/storytelling/timeseries` → params: `familia`, `series_key`

```python
from fastapi import APIRouter, Query
from data_sources.storytelling_loader import (
    get_kpi_snapshot,
    get_alerts_by_status,
    get_family_timeseries,
)

router = APIRouter(prefix=\"/storytelling\")

@router.get(\"/kpis\")
def kpis():
    return get_kpi_snapshot()

@router.get(\"/alerts\")
def alerts(status: list[str] = Query(None)):
    return get_alerts_by_status(statuses=status).to_dict(orient=\"records\")

@router.get(\"/timeseries\")
def timeseries(familia: str):
    return get_family_timeseries(familia).to_dict(orient=\"records\")\n```\n

