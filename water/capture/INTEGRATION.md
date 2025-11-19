# MOF Water Capture – Integration Guide

**Deep-Containment Architecture (DCA) Project**

This guide explains how MOF datasets are integrated with RealityStream ML CoLab reports and the team/projects AI insights viewer.

---

## Quick Access URLs

### View Data in Team/Projects Viewer

**MOF Features** (material properties):
```
https://model.earth/team/projects/#list=mof-features
```

**MOF Targets** (water uptake classification):
```
https://model.earth/team/projects/#list=mof-targets
```

### Run Analysis in RealityStream

Access RealityStream and select from dropdown:
```
https://model.earth/realitystream/
```

**Available Parameters**:
- **MOF Water Capture (All Counties)** - Full dataset analysis
- **MOF Datacenter Locations (5 States)** - NV, CA, TX, AZ, UT focus
- **MOF Optimization (Integrated Dataset)** - ML-ready integrated data

---

## Python Integration Pipeline

### Setup

```bash
cd grid/water/capture

# Install dependencies
pip install -r requirements.txt
```

### Run Integration

```bash
python3 mof_integration.py
```

**Output**:
```
MOF Water Capture - Data Integration Pipeline
============================================================

1. Loading MOF datasets...
   ✓ Loaded 7 MOF samples

2. Simulating adsorption isotherms...
   ✓ Daily yield estimate: 0.69 L/kg/day

3. Optimizing for datacenter locations...
   ✓ Top MOF: FIPS 1005
   ✓ Performance score: 2.714

4. Exporting for RealityStream ML pipeline...
   ✓ Exported integrated dataset
   ✓ Exported AI insights

5. Integration Summary
   Dataset: MOF Water Capture
   Samples: 7
   Features: 8
   Key findings: 3
   Recommendations: 1
```

### Generated Files

1. **`realitystream_data/mof-integrated-dataset.csv`**
   - Merged features + targets
   - ML-ready format for RealityStream CoLab

2. **`realitystream_data/mof-ai-insights.json`**
   - AI insights for team/projects viewer
   - Feature statistics, key findings, recommendations

---

## Integration Architecture

```
DATA SOURCES
├── MOF Features (mof/features/mof-features.csv)
│   └── Properties: surface_area, pore_volume, hydrophilicity, etc.
└── MOF Targets (mof/targets/mof-targets-water-uptake.csv)
    └── Binary classification: 0=Low, 1=High uptake

        ↓ Python Processing (mof_integration.py)

SIMULATION & OPTIMIZATION
├── Adsorption Isotherm Simulation
│   ├── Langmuir model
│   ├── Freundlich model
│   └── Toth model
├── High-Altitude Optimization
│   ├── Sea level (60% humidity)
│   ├── Low altitude (50% humidity)
│   ├── Mid altitude (40% humidity)
│   └── High altitude (30% humidity)
└── AI Insights Generation

        ↓ Output Integration

VISUALIZATION PLATFORMS
├── RealityStream ML CoLab
│   ├── parameters-mof.yaml
│   ├── parameters-datacenter-locations.yaml
│   └── parameters-mof-optimization.yaml
└── Team/Projects Viewer
    ├── mof-features dataset
    ├── mof-targets dataset
    └── AI insights JSON
```

---

## Current Results

### Top Performing MOFs

**By Surface Area**:
- FIPS 1005: 4,100 m²/g
- FIPS 1004: 1,850 m²/g
- FIPS 1006: 1,630 m²/g

**By Daily Water Yield**:
- FIPS 1005: 4.56 L/kg/day
- FIPS 1004: 1.80 L/kg/day
- FIPS 1006: 1.54 L/kg/day

**Most Cost-Effective**:
- FIPS 1005: 0.076 yield/cost ratio
- FIPS 1004: 0.045 yield/cost ratio
- FIPS 1006: 0.044 yield/cost ratio

### Key Recommendations

1. **Thermal Stability**: Prioritize MOFs with thermal stability >600K for reliable temperature-swing operation
2. **Hydrophilicity**: Select MOFs with hydrophilicity >0.7 for low-humidity datacenter locations
3. **Cost Optimization**: FIPS 1005 offers best performance/cost balance

---

## Next Steps

### Phase 1: Expand Dataset (In Progress)
- [ ] Integrate MIT MOF database materials
- [ ] Add real atmospheric data from NOAA
- [ ] Map to actual AI datacenter locations (NV, CA, TX, AZ, UT)

### Phase 2: ML Enhancement
- [ ] Create Jupyter notebook for interactive analysis
- [ ] Train advanced ML models (XGBoost, Neural Networks)
- [ ] Implement SHAP for feature importance

### Phase 3: Rust Integration (Future)
- [ ] Develop thermal-fluid dynamics module
- [ ] Model deep SMR containment designs
- [ ] High-performance simulation engine

---

## Technical Details

### Python Classes

#### MOFAdsorptionSimulator
Simulates water uptake using three isotherm models:

**Langmuir**: `q = (q_max * K * P) / (1 + K * P)`
- Best for monolayer adsorption
- Parameters estimated from MOF properties

**Freundlich**: `q = K_f * P^(1/n)`
- Empirical model for heterogeneous surfaces
- Good for rough performance estimates

**Toth**: `q = q_max * (b * P) / (1 + (b * P)^t)^(1/t)`
- Advanced 3-parameter model
- Most accurate for real MOF behavior

#### HighAltitudeOptimizer
Calculates performance scores based on:
- **Humidity Factor** (30%): Hydrophilicity / ambient humidity
- **Temperature Factor** (25%): Thermal stability / operating temp
- **Capacity Factor** (25%): Surface area × pore volume
- **Cost Factor** (20%): Inverse of normalized cost

#### RealityStreamIntegrator
Handles data export and insight generation:
- Loads features/targets from GitHub URLs
- Merges datasets on FIPS codes
- Generates statistical summaries
- Creates AI insight JSON

---

## Share Progress on X.com

Template for progress updates:

```
🌊 MOF Water Capture - DCA Project

✅ Python adsorption isotherm simulation live
✅ High-altitude optimization (4 altitude bands)
✅ RealityStream ML integration complete
✅ Team/Projects AI insights connected

Top performer: 4.56 L/kg/day water yield

Dataset: https://model.earth/team/projects/#list=mof-features
Analysis: https://model.earth/realitystream/

#DeepContainment #MOF #AIDatacenters #WaterScarcity
```

---

## References

- **RealityStream**: https://github.com/ModelEarth/realitystream
- **Team Projects**: https://github.com/ModelEarth/team
- **Grid Repo**: https://github.com/ModelEarth/grid
- **Python Script**: `mof_integration.py`
- **YAML Params**: `realitystream/parameters/parameters-mof.yaml`
