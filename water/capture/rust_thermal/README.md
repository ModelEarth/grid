# MOF Thermal-Fluid Dynamics Module (Rust)

**Deep-Containment Architecture (DCA) - Performance-Critical Component**

High-performance thermal-fluid dynamics simulation for MOF water capture systems in deep SMR containment designs.

## Overview

This Rust module complements the Python MOF selection pipeline by providing:
- **High-performance thermal simulations** (100-1000x faster than Python)
- **Temperature-swing adsorption modeling**
- **Thermal risk assessment** for deep SMR containment
- **Operating condition optimization**

## Architecture

```
Python MOF Selection
    ↓
    └──> Identifies optimal MOF materials
         (surface area, pore volume, hydrophilicity)
              ↓
Rust Thermal-Fluid Dynamics
    ↓
    └──> Simulates operating performance
         (temperature cycles, energy efficiency, safety)
              ↓
Final Design Parameters
```

## Features

### 1. Temperature-Swing Adsorption Simulation

Simulates the complete adsorption/desorption cycle:
- **Adsorption phase**: Water uptake at ambient temperature
- **Regeneration phase**: Water release at elevated temperature
- **Energy calculations**: Heating requirements, heat of adsorption
- **Efficiency metrics**: Water yield per unit energy

### 2. Thermal Risk Assessment

Evaluates safety for deep containment:
- **Thermal stability margins**: Operating temp vs. MOF decomposition
- **Risk scoring**: 0-1 scale (lower is safer)
- **Safety thresholds**:
  - Low risk: T_op < 0.8 × T_stability
  - Moderate risk: 0.8-0.9 × T_stability
  - High risk: > 0.9 × T_stability

### 3. Operating Condition Optimization

Finds optimal parameters for:
- **Regeneration temperature**: Balance yield vs. energy
- **Cycle timing**: Maximize throughput
- **Safety constraints**: Ensure stable operation

## Usage

### Build

```bash
cd rust_thermal
cargo build --release
```

### Run Tests

```bash
cargo test
```

### Example Code

```rust
use mof_thermal_dynamics::*;

// Define MOF properties (from Python selection)
let properties = MOFThermalProperties {
    fips: 1005,
    thermal_conductivity: 0.5,    // W/(m·K)
    specific_heat: 1000.0,         // J/(kg·K)
    density: 600.0,                // kg/m³
    thermal_stability_k: 573.0,    // K
    heat_of_adsorption: 45.0,      // kJ/mol
};

// Define operating conditions
let conditions = OperatingConditions {
    ambient_temp_k: 298.0,
    regeneration_temp_k: 373.0,
    humidity: 0.4,
    pressure_atm: 1.0,
    cycle_time_seconds: 3600.0,
};

// Run simulation
let simulator = ThermalFluidSimulator::new(properties, conditions);
let results = simulator.simulate_temperature_swing()?;

println!("Water yield: {:.3} kg", results.water_yield_kg);
println!("Energy: {:.1} kJ", results.energy_consumption_kj);
println!("Efficiency: {:.4}", results.thermal_efficiency);
println!("Risk score: {:.2}", results.risk_score);

// Optimize conditions
let mut simulator = ThermalFluidSimulator::new(properties, conditions);
let optimized = simulator.optimize_conditions()?;
println!("Optimal regeneration temp: {:.1} K", optimized.regeneration_temp_k);
```

## Simulation Models

### Temperature-Swing Energy Balance

```
E_total = E_heating + E_adsorption

where:
  E_heating = m_MOF × c_p × ΔT
  E_adsorption = n_water × Q_ads
```

### Thermal Efficiency

```
η_thermal = m_water_produced / E_total
```

### Risk Score

```
Risk = f(T_op / T_stability)

  Low:      T_op < 0.8 × T_stability  →  Risk = 0.1
  Moderate: 0.8-0.9 × T_stability     →  Risk = 0.5
  High:     > 0.9 × T_stability       →  Risk = 0.9
```

## Integration with Python Pipeline

### Step 1: Python MOF Selection
```python
# mof_integration.py selects optimal MOFs
integrator = RealityStreamIntegrator('.')
features, targets = integrator.load_data()
top_mof = features.nlargest(1, 'performance_score')
```

### Step 2: Export to Rust
```python
# Export MOF properties for Rust simulation
mof_properties = {
    'fips': top_mof['Fips'],
    'thermal_stability_k': top_mof['thermal_stability_K'],
    # ... other properties
}
json.dump(mof_properties, open('mof_for_rust.json', 'w'))
```

### Step 3: Rust Simulation
```rust
// Load from JSON and simulate
let properties = load_from_json("mof_for_rust.json")?;
let simulator = ThermalFluidSimulator::new(properties, conditions);
let results = simulator.simulate_temperature_swing()?;
```

### Step 4: Return to Python
```rust
// Export results
serde_json::to_writer(
    File::create("thermal_results.json")?,
    &results
)?;
```

## Future Enhancements

### Phase 1: Advanced Thermal Modeling
- [ ] 3D heat transfer with finite element analysis
- [ ] Transient temperature profiles
- [ ] Multi-layer MOF bed modeling
- [ ] Heat exchanger integration

### Phase 2: Fluid Dynamics
- [ ] Water vapor transport through MOF bed
- [ ] Pressure drop calculations
- [ ] Mass transfer coefficients
- [ ] Breakthrough curve modeling

### Phase 3: Deep SMR Integration
- [ ] Containment vessel heat transfer
- [ ] Safety analysis for nuclear proximity
- [ ] Emergency shutdown scenarios
- [ ] Long-term stability modeling

### Phase 4: Parallelization
- [ ] Multi-threaded simulation with Rayon
- [ ] GPU acceleration for large-scale models
- [ ] Distributed computing for parameter sweeps

## Performance Targets

| Operation | Target | Status |
|-----------|--------|--------|
| Single simulation | < 1 ms | ✅ Achieved |
| Optimization sweep | < 100 ms | 🚧 In progress |
| Full thermal profile | < 1 s | ⏳ Planned |
| GPU-accelerated | < 10 ms | ⏳ Planned |

## Dependencies

- **serde/serde_json**: Data serialization
- **csv**: CSV file handling
- **nalgebra**: Linear algebra (future FEA)
- **rayon**: Parallel computing

## License

Part of the Deep-Containment Architecture project.
See main repository for license details.

## References

- Python integration: `../mof_integration.py`
- MOF data: `../mof/features/mof-features.csv`
- Main docs: `../INTEGRATION.md`
