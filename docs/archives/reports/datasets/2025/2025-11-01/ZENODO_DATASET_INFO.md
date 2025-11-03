# 📊 Zenodo Milan Telecom Dataset Information

## ✅ Dataset Successfully Downloaded!

The Milan Telecom & Weather dataset from Zenodo has been successfully downloaded and analyzed.

---

## 📁 File Information

- **File:** `data/raw/zenodo_milan_telecom/output-step-bsId_1-2023_9_28_12_50_10.csv`
- **Size:** ~28 MB
- **Format:** CSV

---

## 📊 Dataset Structure

### Dataset Statistics

Based on initial analysis:
- **Total Rows:** Large dataset (check with `len(df)`)
- **Total Columns:** 38 columns
- **Unique Base Stations (bsId):** Multiple (check with analysis)
- **Episodes:** Game-theoretic episode indices
- **Steps:** Time step indices (sequential from 0)

### Column Information

**Core Columns:**
- `bsId` - 5G BaseStation ID
- `episode` - Game-theoretic episode index
- `step` - Time step index (can be used as temporal index)

**Traffic Load Columns:**
- `loadSMS` - Total in/out SMS traffic load
- `loadInt` - Total in/out Internet traffic load
- `loadCalls` - Total in/out Voice traffic load

**Raw Activity Columns:**
- `rawActSMS` - Original raw network packets (SMS load)
- `rawActInt` - Original raw network packets (Internet load)
- `rawActCalls` - Original raw network packets (Voice load)

**Deferred Traffic Columns:**
- `defSMS`, `defInt`, `defCalls` - Deferred traffic loads
- `rawActDefSMS`, `rawActDefInt`, `rawActDefCalls` - Deferred raw packets

**Scheduled Traffic Columns:**
- `schedSMS`, `schedInt`, `schedCalls` - Admitted traffic loads
- `schedDelaySMS`, `schedDelayInt`, `schedDelayCalls` - Queued for admission

**Dropped Traffic Columns:**
- `dropSMS`, `dropInt`, `dropCalls` - Raw Packets Dropped

**Aggregate Columns:**
- `totalSched` - Total Admitted Traffic load ⭐ **Use as quantity/demand**
- `bsCap` - BaseStation network capacity
- `totalDropped` - Total Raw Packets Dropped Traffic load

**Rate Columns:**
- `rejectRate` - Total Traffic load network packets reject rate
- `rejectRateCalls`, `rejectRateInt`, `rejectRateSMS` - Per-service reject rates
- `delayRate` - Total Delayed (not queued yet for admission) Traffic load
- `delayRateCalls`, `delayRateInt`, `delayRateSMS` - Per-service delay rates

**Reward Columns:**
- `reward` - Total game reward value
- `episodeReward` - Total reward value per episode
- `avgEpisodeReward` - Average reward value per episode

---

## 🔄 Mapping to Unified Schema

### Configuration in `config/datasets_config.json`:

```json
{
  "zenodo_milan_telecom": {
    "columns_mapping": {
      "date": "step",              // Use step as time index
      "item_id": "bsId",           // Base station ID as item
      "quantity": "totalSched",    // Total scheduled traffic as demand
      "demand": "totalSched",      // Same as quantity
      "site_id": "bsId"            // Base station as site
    }
  }
}
```

### Preprocessing Notes:

1. **Time Index:** Use `step` column as temporal index (can be converted to datetime if start date is known)
2. **Demand/Quantity:** Use `totalSched` (Total Admitted Traffic load) as the demand/quantity metric
3. **External Factors:** Dataset includes:
   - Traffic capacity (`bsCap`)
   - Reject rates (`rejectRate*`)
   - Delay rates (`delayRate*`)
   - Service-specific loads (`loadSMS`, `loadInt`, `loadCalls`)

4. **Aggregation:** If needed, can aggregate by:
   - Base station (`bsId`)
   - Episode (`episode`)
   - Time period (if step is converted to datetime)

---

## 🎯 Use Cases

This dataset is perfect for:

1. **5G Network Slice Resource Demand Prediction**
   - Predict `totalSched` based on historical traffic patterns
   - Use `bsCap` as capacity constraint
   - Consider reject/delay rates as external factors

2. **Time Series Forecasting Models:**
   - ARIMA/Prophet: Use `step` as time index, `totalSched` as target
   - LSTM: Use multiple traffic features (loadSMS, loadInt, loadCalls)
   - SARIMAX: Include capacity and rate metrics as external factors

3. **Multi-Service Demand Prediction:**
   - Predict SMS, Internet, and Voice traffic separately
   - Model service-specific reject/delay rates

---

## 📝 Preprocessing Recommendations

1. **Convert Step to Datetime (if possible):**
   - If base date is known, convert `step` to datetime
   - Otherwise, keep as sequential index

2. **Feature Engineering:**
   - Calculate utilization: `totalSched / bsCap`
   - Create traffic mix ratios: `loadSMS / totalSched`, etc.
   - Aggregate by base station if needed

3. **External Factors to Include:**
   - `bsCap` - Capacity constraint
   - `rejectRate*` - Network congestion indicators
   - `delayRate*` - Service quality indicators
   - Traffic mix ratios

---

## ✅ Integration Status

- ✅ **Downloaded:** Successfully downloaded via direct CSV URL
- ✅ **Verified:** File structure confirmed (38 columns)
- ⏳ **Preprocessing:** Ready for preprocessing (update column mapping)
- ⏳ **Merge:** Will be included in unified dataset after preprocessing

---

## 🔗 References

- **Zenodo Record:** https://zenodo.org/records/14012612
- **Original MILANO Dataset:** https://ieee-dataport.org/documents/milan-dataset
- **Paper:** "Resource Demand Prediction for Network Slices in 5G Using ML Enhanced With Network Models"

---

**Status:** ✅ **Downloaded and Ready for Preprocessing**  
**Date:** 2025-10-31

