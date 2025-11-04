# 🎨 FRONTEND CLUSTER - 4-DAY SPRINT PLAN
## Nova Corrente - Dashboard UI

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** 🚀 Execution-Ready  
**Sprint:** 4 Days (D0-D4)  
**Cluster Lead:** Frontend Lead  
**Team Size:** 1-2 Engineers

---

## 📋 QUICK ORIENTATION

**Goal:** Minimal, fast dashboard with key visuals and drilldown. Single-page app (React + Vite) consuming the BFF.

**Key Constraint:** Small bundle size (< 500KB gzipped), fast load time (< 2.5s), simple charts (Recharts or Chart.js), NO ML processing UI.

**Reference Documents:**
- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - API endpoints
- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - Data requirements
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy

---

## 🔒 GLOBAL STRATEGIC CONSTRAINT — "NO ML OPS LOGIC IN DEPLOYMENT"

**Reference:** [Global Constraints Document](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md)

**Policy:** All Machine Learning (ML) processing, training, and predictive computations remain strictly **off the production deployment path**. Only **precomputed analytical insights** are displayed in the UI.

**Frontend Cluster Specific Rules:**
- ✅ Display analytical insights only—no real-time predictions or retraining triggers
- ✅ "Last updated" timestamp on each chart to communicate data freshness (from `generated_at` field)
- ✅ Optional "Refresh Data" button (admin only) for manual data refresh (hooked to backend trigger)
- ❌ **NO ML processing UI** components
- ❌ **NO real-time prediction** or model training UI
- ❌ **NO ML libraries** in bundle (keep < 500KB gzipped)

**Validation:**
- [ ] Check UI components have NO ML processing triggers
- [ ] Verify "Last updated" timestamp visible on all charts
- [ ] Verify refresh data button works (admin only)
- [ ] Check bundle size < 500KB (NO ML libraries)

---

## 🎯 KEY CONSTRAINTS & ASSUMPTIONS

### Technical Stack
- ✅ **Framework:** React + Vite (already exists)
- ✅ **Styling:** Tailwind CSS (for speed)
- ✅ **Charts:** Recharts or Chart.js (simple)
- ✅ **State:** React hooks (useState, useEffect)
- ✅ **Caching:** Local cache (TTL 60s)
- ❌ **Deferred:** Redux, complex routing, SSR
- ❌ **NO ML libraries:** No TensorFlow.js, no ML processing libraries

### UX Requirements
- **Dashboard Page 1:** Forecast accuracy per item (chart) + table of top-k understock/overstock
- **Drilldown:** Click item → timeseries line chart of forecast vs actual + date range controls
- **Authentication:** Simple token in local storage (no complex SSO)
- **Data Freshness:** Display "Last updated" timestamp from ML metadata

---

## 📅 DELIVERABLES (DAY-BY-DAY)

### **D0 (TODAY): Freeze UX & Component List** ⏱️ 2-4 hours
**Owner:** Frontend Lead  
**Deliverables:**
- [ ] Static mockups (very small): header, signin token box, dashboard main, item detail
- [ ] Component list (see below)
- [ ] API contract review (align with Backend)
- [ ] Design tokens (colors, spacing, typography)
- [ ] **Verify NO ML processing UI** in mockups

**Component List:**
- `Header` - Navigation, auth token input
- `Dashboard` - Main dashboard page
- `ItemList` - List of items with metadata
- `ItemDetail` - Item drilldown with timeseries chart (precomputed data)
- `ForecastChart` - Line chart (forecast vs actual) - **PRECOMPUTED DATA**
- `SummaryTable` - Table of top items
- `LastUpdated` - Timestamp component (from ML metadata)
- `RefreshDataButton` - Admin-only data refresh trigger

**Output Files:**
- `frontend/docs/mockups/` - Static mockups
- `frontend/docs/components.md` - Component list

---

### **D1: Project Scaffold + Components** ⏱️ 6-8 hours
**Owner:** 1-2 Frontend Engineers  
**Deliverables:**

#### Project Setup
- [ ] Scaffold React + Vite (if not exists)
- [ ] Setup Tailwind CSS
- [ ] Create `APIClient` wrapper for endpoints
- [ ] Configure environment variables (`.env`)
- [ ] **Verify NO ML libraries** in package.json

#### Core Components
- [ ] Implement `Header` component (navigation, auth token input)
- [ ] Implement `ItemList` component (list items with metadata)
- [ ] Implement `LastUpdated` component (displays generated_at from API)
- [ ] Implement basic layout structure

**Acceptance Criteria:**
- ✅ React + Vite project scaffolded
- ✅ Tailwind CSS configured
- ✅ API client connects to backend
- ✅ Components render without errors
- ✅ NO ML libraries in dependencies

**Output Files:**
- `frontend/src/components/Header.tsx`
- `frontend/src/components/ItemList.tsx`
- `frontend/src/components/LastUpdated.tsx`
- `frontend/src/lib/api.ts` - API client
- `frontend/.env.example` - Environment variables

**Technical Specs:**
```typescript
// Example API Client - NO ML endpoints
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export const apiClient = {
  getItems: () => axios.get(`${API_BASE_URL}/api/v1/items`),
  getTimeseries: (id: string, start: string, end: string) =>
    axios.get(`${API_BASE_URL}/api/v1/items/${id}/timeseries`, { params: { start, end } }),
  getForecastSummary: (start: string, end: string) =>
    axios.get(`${API_BASE_URL}/api/v1/forecasts/summary`, { params: { start, end } }),
  refreshData: () => axios.post(`${API_BASE_URL}/api/v1/data/refresh`), // Admin only
  // NO ML endpoints: /predict, /forecast, /train, /retrain
};
```

---

### **D2: Charts + Interactions** ⏱️ 6-8 hours
**Owner:** 1 Frontend Engineer  
**Deliverables:**

#### Chart Components
- [ ] Install chart library (Recharts or Chart.js) - **NO ML libraries**
- [ ] Implement `ForecastChart` component (line chart: forecast vs actual) - **PRECOMPUTED DATA**
- [ ] Implement `SummaryTable` component (table of top items) - **PRECOMPUTED DATA**
- [ ] Add date range picker (start/end date inputs)
- [ ] Add **"Last updated" timestamp** on each chart (from `generated_at` field in API response)
- [ ] Implement caching on client (local cache TTL 60s)
- [ ] Add optimistic loading (skeleton states)
- [ ] **NO real-time prediction UI** - only display precomputed results

**Acceptance Criteria:**
- ✅ Charts render with correct data
- ✅ "Last updated" timestamp visible
- ✅ Date range picker works
- ✅ Caching works (60s TTL)
- ✅ Loading states work
- ✅ NO ML processing UI components

**Output Files:**
- `frontend/src/components/ForecastChart.tsx`
- `frontend/src/components/SummaryTable.tsx`
- `frontend/src/components/DateRangePicker.tsx`
- `frontend/src/lib/cache.ts` - Client-side caching

**Technical Specs:**
```typescript
// Example Chart Component - PRECOMPUTED DATA
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface TimeseriesData {
  date: string;
  forecast: number;
  actual: number;
  source: string;
  model_version?: string;
  generated_at?: string;
}

interface ForecastChartProps {
  data: TimeseriesData[];
  lastUpdated?: string; // From API metadata
}

export const ForecastChart = ({ data, lastUpdated }: ForecastChartProps) => {
  return (
    <div>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="forecast" stroke="#8884d8" name="Forecast" />
        <Line type="monotone" dataKey="actual" stroke="#82ca9d" name="Actual" />
      </LineChart>
      {lastUpdated && (
        <div className="text-sm text-gray-500 mt-2">
          Last updated: {new Date(lastUpdated).toLocaleString()}
        </div>
      )}
    </div>
  );
};
```

---

### **D3: Responsiveness & Polish** ⏱️ 6-8 hours
**Owner:** 1 Frontend Engineer  
**Deliverables:**

#### UX Improvements
- [ ] Add loading states (skeleton loaders, spinners)
- [ ] Add error handling (error messages, retry buttons)
- [ ] Add minimal accessibility (ARIA labels, keyboard navigation)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Add **"Refresh Data" button** (admin only, triggers backend refresh endpoint)
- [ ] Add E2E smoke test (Playwright or Cypress minimal)
- [ ] **Verify NO ML processing UI** in final components

**Acceptance Criteria:**
- ✅ Loading states visible
- ✅ Error handling works
- ✅ Accessibility basics implemented
- ✅ Responsive design works
- ✅ Refresh data button works (admin only)
- ✅ NO ML processing UI

**Output Files:**
- `frontend/src/components/Loading.tsx`
- `frontend/src/components/Error.tsx`
- `frontend/src/components/RefreshDataButton.tsx`
- `frontend/tests/e2e/smoke.test.ts` - E2E tests

---

### **D4: Bundle & Integration Test** ⏱️ 4-6 hours
**Owner:** 1 Frontend Engineer  
**Deliverables:**

#### Integration & Deployment
- [ ] Integrate with deployed backend (staging URLs)
- [ ] Test all flows (dashboard load, item drilldown, date range)
- [ ] Optimize bundle size (< 500KB gzipped)
- [ ] Add build scripts (production build, Dockerfile)
- [ ] Test deployment (Docker or static hosting)
- [ ] **Verify bundle size** (NO ML libraries)

**Acceptance Criteria:**
- ✅ Integration with backend works
- ✅ All flows tested and working
- ✅ Bundle size < 500KB gzipped
- ✅ Production build successful
- ✅ NO ML libraries in bundle

**Output Files:**
- `frontend/Dockerfile` - Dockerfile for deployment
- `frontend/dist/` - Production build
- `frontend/.env.production` - Production environment variables

---

## ✅ SUCCESS CRITERIA (ACCEPTANCE TESTS)

### Functional Requirements
- [ ] ✅ Page load time < 2.5s on reasonable dev VM
- [ ] ✅ Charts render with correct values for last 30 days
- [ ] ✅ Drilldown returns within 1.5s for cached queries
- [ ] ✅ All API endpoints consumed correctly
- [ ] ✅ Error handling works (network errors, invalid data)
- [ ] ✅ "Last updated" timestamp visible on all charts

### Performance Requirements
- [ ] ✅ Bundle size < 500KB gzipped
- [ ] ✅ First contentful paint < 1.5s
- [ ] ✅ Time to interactive < 2.5s

### ML Ops Validation (MANDATORY)
- [ ] ✅ No ML processing UI components
- [ ] ✅ Only display precomputed analytical data
- [ ] ✅ "Last updated" timestamp visible on all charts
- [ ] ✅ Refresh data button works (admin only)
- [ ] ✅ No real-time prediction or training UI
- [ ] ✅ Bundle size < 500KB (NO ML libraries)

### UX Requirements
- [ ] ✅ Responsive design (mobile, tablet, desktop)
- [ ] ✅ Loading states visible
- [ ] ✅ Error messages clear and actionable

---

## 🚨 SCOPE-REDUCTION OPTIONS (IF BLOCKERS)

### Option 1: Absolute Minimal (Static HTML)
**Trigger:** React/Vite setup fails or too complex

**Changes:**
- Serve static HTML page that fetches JSON endpoints
- Use vanilla JavaScript for API calls
- No SPA routing, simpler structure

**Impact:** ⚠️ Less interactive, but functional for demo

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 2: No Chart Library (SVG/D3 Micro)
**Trigger:** Chart library too large or bundle size issue

**Changes:**
- Remove chart library
- Use small SVG/D3 micro charts
- Custom chart components

**Impact:** ⚠️ More code, but smaller bundle

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

### Option 3: Minimal Responsiveness (Desktop Only)
**Trigger:** Time pressure or responsive issues

**Changes:**
- Focus on desktop view only
- Mobile layout minimal (basic scaling)
- Faster to deploy

**Impact:** ⚠️ Poor mobile experience, but functional for desktop

**Constraint Compliance:** ✅ Still compliant (no ML processing)

---

## 🔗 KEY RECOMMENDATIONS

### Technical Decisions
1. **Use Recharts** - Simple, lightweight, React-friendly
2. **Client-side caching** - Reduce API calls, faster UX
3. **Optimistic loading** - Better perceived performance
4. **Tailwind CSS** - Fast styling, small bundle
5. **Display ML metadata** - Show model_version and generated_at for transparency

### Follow-Up Questions (Answer Quickly)
1. **Chart Library:** Recharts or Chart.js? (Recharts recommended)
2. **Bundle Size:** Target < 500KB gzipped acceptable?
3. **Responsive:** Desktop-only OK for MVP, or need mobile?
4. **Deployment:** Static hosting (Vercel/Netlify) or Docker?
5. **Admin UI:** Need admin panel for data refresh, or API key only?

---

## 📚 REFERENCE LINKS

- [Backend Cluster](./02_BACKEND_CLUSTER_4DAY_SPRINT_PT_BR.md) - API endpoints
- [Data Cluster](./01_DATA_CLUSTER_4DAY_SPRINT_PT_BR.md) - Data requirements
- [Global Constraints](./GLOBAL_CONSTRAINTS_NO_ML_OPS_PT_BR.md) - Complete policy
- [Deploy Cluster](./04_DEPLOY_CLUSTER_4DAY_SPRINT_PT_BR.md) - Deployment requirements

---

## 📝 NEXT STEPS

1. **Assign Cluster Lead:** Frontend Lead
2. **Assign Team:** 1-2 Engineers
3. **Kickoff Meeting:** Review mockups, align with Backend
4. **Daily Standup:** 9 AM - Review progress, blockers
5. **End of Day:** Acceptance test for each day's deliverables

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Execution-Ready - 4-Day Sprint Plan

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

