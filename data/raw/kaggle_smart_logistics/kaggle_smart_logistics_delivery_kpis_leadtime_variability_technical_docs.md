# 📊 CONTEXT & TECHNICAL DOCUMENTATION
## Kaggle Smart Logistics Dataset

**Dataset ID:** `kaggle_smart_logistics`  
**Source:** Kaggle  
**Status:** ✅ Processed (if applicable)  
**Relevance:** ⭐⭐⭐ (Medium - Delivery KPIs, Some Relevance)

---

## 📋 OVERVIEW

### Dataset Description

**Purpose:** Smart Logistics Operations & Delivery KPIs  
**Records:** 3,200+ rows  
**Features:** 15 columns (timestamp, asset_id, location, inventory, shipment, temperature, humidity, traffic, delay, etc.)  
**Date Range:** 2024-01-18+ (sample data)  
**Target Variable:** `Logistics_Delay` - Delivery delay indicator (0=on-time, 1=delayed)

**Business Context:**
- Smart logistics operations
- Delivery delay prediction
- Asset tracking (trucks, vehicles)
- Climate factors (temperature, humidity)
- Traffic conditions
- **Delivery KPIs** → Supplier lead time impact

---

## 🔗 SOURCE REFERENCES

### Primary Source

**Platform:** Kaggle  
**Dataset ID:** Smart logistics dataset  
**URL:** https://www.kaggle.com/datasets/smart-logistics  
**License:** Open Database License (ODbL)

---

## 📊 DATA STRUCTURE

### Column Description

| Column | Type | Description | Business Context |
|--------|------|-------------|------------------|
| `Timestamp` | DateTime | Timestamp | Temporal key |
| `Asset_ID` | String | Truck_1, Truck_2, etc. | Vehicle identifier |
| `Latitude` | Float | -65 to 82 | GPS latitude | Location |
| `Longitude` | Float | -154 to 147 | GPS longitude | Location |
| `Inventory_Level` | Integer | 100-500 | Inventory level | Stock level |
| `Shipment_Status` | String | Delayed, In Transit, Delivered | Delivery status | **Lead time impact ⭐** |
| `Temperature` | Float | 20-30 °C | Temperature | Climate factor |
| `Humidity` | Float | 40-80% | Humidity | Climate factor |
| `Traffic_Status` | String | Clear, Heavy, Detour | Traffic condition | Delivery delay |
| `Waiting_Time` | Integer | 0-60 minutes | Waiting time | Delivery delay |
| `User_Transaction_Amount` | Float | 100-500 | Transaction amount | Order size |
| `User_Purchase_Frequency` | Integer | 2-10 | Purchase frequency | Order frequency |
| `Logistics_Delay_Reason` | String | None, Weather, Traffic, Mechanical Failure | Delay reason | **Lead time variability ⭐** |
| `Asset_Utilization` | Float | 60-100% | Asset utilization | Efficiency metric |
| `Demand_Forecast` | Float | 100-300 | Demand forecast | ML forecast |
| `Logistics_Delay` | Integer | 0, 1 | **TARGET: Delay indicator** | **Lead time impact ⭐** |

---

## 🎯 USE CASE FOR NOVA CORRENTE

### Relevance Analysis

**Strengths:**
- ✅ **Delivery delay prediction** → Lead time variability
- ✅ Climate factors (temperature, humidity) - relevant for Salvador, BA
- ✅ Traffic conditions (delivery delays)
- ✅ Supplier lead time impact

**Adaptation Strategy:**
```python
# Logistics Delay → Lead Time Variability
def logistics_delay_to_lead_time_variability(delay_reason, temperature, humidity, traffic):
    """
    Maps logistics delay to lead time variability for Nova Corrente
    """
    # Base lead time variability
    base_variability = {
        'None': 0.0,      # No delay
        'Weather': 3.0,   # +3 days (rain, humidity in Salvador)
        'Traffic': 1.0,   # +1 day
        'Mechanical Failure': 5.0  # +5 days (equipment failure)
    }
    
    # Climate adjustment (Salvador-specific)
    if temperature > 30 and humidity > 80:  # Hot and humid (Salvador common)
        climate_adjustment = 1.5  # +50% delay
    else:
        climate_adjustment = 1.0
    
    variability = base_variability.get(delay_reason, 0.0) * climate_adjustment
    
    return variability

# Example: Weather delay, hot and humid (Salvador)
delay_reason = 'Weather'
temperature = 32  # Hot
humidity = 85  # High humidity

variability = logistics_delay_to_lead_time_variability(delay_reason, temperature, humidity, 'Clear')
# Result: 3.0 * 1.5 = 4.5 days additional lead time
```

---

## 📁 FILE LOCATION

**Raw Data:**
- `data/raw/kaggle_smart_logistics/smart_logistics_dataset.csv` (~800 KB, 3,200+ rows)

**Processed Data:**
- `data/processed/kaggle_smart_logistics_preprocessed.csv` (if applicable)

---

## 📝 NOTES

**Last Updated:** 2025-11-01  
**Maintained By:** Nova Corrente Demand Forecasting Team  
**Status:** ⚠️ Medium relevance - Delivery KPIs useful for lead time variability, but generic logistics focus

**Key Insight:** Logistics delays → Lead time variability. Weather delays in Salvador (high humidity) cause +3-5 days lead time increases.

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

