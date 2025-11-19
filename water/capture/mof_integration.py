"""
MOF Water Capture - Data Integration & Analysis
Deep-Containment Architecture (DCA) Project

This script integrates MOF datasets with RealityStream ML pipeline and team/projects viewer.
Simulates MOF adsorption isotherms using NumPy/SciPy for high-altitude water yield optimization.

Author: Integration for DCA Project
Features:
- MOF adsorption isotherm simulation
- High-altitude water yield optimization
- RealityStream ML data preparation
- AI insights data generation
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import json
from pathlib import Path
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class MOFAdsorptionSimulator:
    """Simulates MOF water adsorption isotherms using Langmuir and Freundlich models"""

    def __init__(self):
        self.models = {
            'langmuir': self.langmuir_isotherm,
            'freundlich': self.freundlich_isotherm,
            'toth': self.toth_isotherm
        }

    @staticmethod
    def langmuir_isotherm(P: np.ndarray, q_max: float, K: float) -> np.ndarray:
        """
        Langmuir adsorption isotherm model
        q = (q_max * K * P) / (1 + K * P)
        """
        return (q_max * K * P) / (1 + K * P)

    @staticmethod
    def freundlich_isotherm(P: np.ndarray, K_f: float, n: float) -> np.ndarray:
        """
        Freundlich adsorption isotherm model
        q = K_f * P^(1/n)
        """
        return K_f * np.power(P, 1/n)

    @staticmethod
    def toth_isotherm(P: np.ndarray, q_max: float, b: float, t: float) -> np.ndarray:
        """
        Toth adsorption isotherm model
        q = q_max * (b * P) / (1 + (b * P)^t)^(1/t)
        """
        return q_max * (b * P) / np.power(1 + np.power(b * P, t), 1/t)

    def simulate_mof_performance(self, mof_properties: Dict,
                                  humidity_range: np.ndarray,
                                  temperature_K: float = 298) -> Dict:
        """
        Simulate MOF water uptake across humidity range

        Args:
            mof_properties: Dict with surface_area, pore_volume, hydrophilicity, etc.
            humidity_range: Array of relative humidity values (0-1)
            temperature_K: Temperature in Kelvin

        Returns:
            Dict with uptake predictions and model parameters
        """
        # Extract MOF properties
        surface_area = mof_properties.get('surface_area_m2g', 1000)
        pore_volume = mof_properties.get('pore_volume_cm3g', 0.5)
        hydrophilicity = mof_properties.get('hydrophilicity', 0.5)
        max_uptake = mof_properties.get('max_water_uptake', 0.3)

        # Estimate Langmuir parameters from MOF properties
        # q_max correlates with pore volume and hydrophilicity
        q_max = max_uptake * (1 + 0.3 * hydrophilicity)

        # K (adsorption equilibrium constant) increases with hydrophilicity
        # and surface area
        K = 5.0 * hydrophilicity * (surface_area / 1000)

        # Simulate water uptake using Langmuir model
        water_uptake = self.langmuir_isotherm(humidity_range, q_max, K)

        # Calculate daily water yield (liters per kg MOF per day)
        # Assuming 4 cycles per day (day/night temperature swing)
        cycles_per_day = 4
        avg_uptake = np.mean(water_uptake)
        daily_yield = avg_uptake * cycles_per_day

        return {
            'humidity': humidity_range.tolist(),
            'water_uptake': water_uptake.tolist(),
            'daily_yield_L_kg_day': daily_yield,
            'q_max': q_max,
            'K': K,
            'model': 'langmuir'
        }


class HighAltitudeOptimizer:
    """Optimizes MOF performance for high-altitude datacenter locations"""

    def __init__(self):
        self.altitude_conditions = {
            'sea_level': {'pressure_atm': 1.0, 'temp_K': 298, 'humidity_avg': 0.6},
            'low_altitude': {'pressure_atm': 0.95, 'temp_K': 295, 'humidity_avg': 0.5},
            'mid_altitude': {'pressure_atm': 0.85, 'temp_K': 288, 'humidity_avg': 0.4},
            'high_altitude': {'pressure_atm': 0.7, 'temp_K': 280, 'humidity_avg': 0.3},
        }

    def optimize_for_location(self, mof_df: pd.DataFrame,
                              location_data: Dict) -> pd.DataFrame:
        """
        Optimize MOF selection for specific datacenter location

        Args:
            mof_df: DataFrame with MOF properties
            location_data: Dict with altitude, humidity, temperature

        Returns:
            DataFrame with optimized MOF rankings
        """
        # Calculate performance scores for each MOF
        mof_df = mof_df.copy()

        altitude_category = self._categorize_altitude(location_data.get('altitude_m', 0))
        conditions = self.altitude_conditions[altitude_category]

        # Performance factors
        # Higher hydrophilicity better for low humidity environments
        humidity_factor = mof_df['hydrophilicity'] / conditions['humidity_avg']

        # Thermal stability important for temperature swing cycles
        temp_factor = np.clip(mof_df['thermal_stability_K'] / conditions['temp_K'], 0.8, 1.2)

        # Surface area and pore volume drive capacity
        capacity_factor = (mof_df['surface_area_m2g'] / 1000) * mof_df['pore_volume_cm3g']

        # Cost efficiency
        cost_factor = 1 / (mof_df['cost_per_kg'] / 50)  # Normalized to $50/kg baseline

        # Combined performance score
        mof_df['performance_score'] = (
            0.3 * humidity_factor +
            0.25 * temp_factor +
            0.25 * capacity_factor +
            0.2 * cost_factor
        )

        # Daily water yield estimate for location
        mof_df['estimated_daily_yield'] = (
            mof_df['max_water_uptake'] *
            conditions['humidity_avg'] *
            4  # cycles per day
        )

        return mof_df.sort_values('performance_score', ascending=False)

    def _categorize_altitude(self, altitude_m: float) -> str:
        """Categorize altitude into performance bands"""
        if altitude_m < 500:
            return 'sea_level'
        elif altitude_m < 1500:
            return 'low_altitude'
        elif altitude_m < 3000:
            return 'mid_altitude'
        else:
            return 'high_altitude'


class RealityStreamIntegrator:
    """Integrates MOF data with RealityStream ML pipeline"""

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.features_path = self.base_path / 'mof' / 'features' / 'mof-features.csv'
        self.targets_path = self.base_path / 'mof' / 'targets' / 'mof-targets-water-uptake.csv'

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load MOF features and targets"""
        features = pd.read_csv(self.features_path)
        targets = pd.read_csv(self.targets_path)
        return features, targets

    def create_integrated_dataset(self) -> pd.DataFrame:
        """Merge features and targets for ML training"""
        features, targets = self.load_data()
        integrated = features.merge(targets, on='Fips', how='left')
        return integrated

    def generate_ai_insights(self, features: pd.DataFrame) -> Dict:
        """
        Generate AI insight data for team/projects viewer

        Returns structured data for AI analysis and visualization
        """
        insights = {
            'dataset_info': {
                'name': 'MOF Water Capture',
                'description': 'Metal-Organic Framework atmospheric water capture for AI datacenters',
                'num_samples': len(features),
                'num_features': len(features.columns) - 1,  # Exclude Fips
            },
            'feature_statistics': {},
            'key_findings': [],
            'recommendations': []
        }

        # Calculate feature statistics
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != 'Fips':
                insights['feature_statistics'][col] = {
                    'mean': float(features[col].mean()),
                    'std': float(features[col].std()),
                    'min': float(features[col].min()),
                    'max': float(features[col].max()),
                    'median': float(features[col].median())
                }

        # Generate key findings
        top_surface_area = features.nlargest(3, 'surface_area_m2g')
        insights['key_findings'].append({
            'finding': 'Top Surface Area MOFs',
            'counties': top_surface_area['Fips'].tolist(),
            'values': top_surface_area['surface_area_m2g'].tolist()
        })

        top_yield = features.nlargest(3, 'daily_water_yield')
        insights['key_findings'].append({
            'finding': 'Highest Daily Water Yield',
            'counties': top_yield['Fips'].tolist(),
            'values': top_yield['daily_water_yield'].tolist()
        })

        # Cost-effectiveness analysis
        features['cost_effectiveness'] = features['daily_water_yield'] / features['cost_per_kg']
        top_cost_effective = features.nlargest(3, 'cost_effectiveness')
        insights['key_findings'].append({
            'finding': 'Most Cost-Effective MOFs',
            'counties': top_cost_effective['Fips'].tolist(),
            'values': top_cost_effective['cost_effectiveness'].tolist()
        })

        # Generate recommendations
        avg_hydrophilicity = features['hydrophilicity'].mean()
        if avg_hydrophilicity < 0.6:
            insights['recommendations'].append(
                "Consider MOFs with higher hydrophilicity (>0.7) for improved low-humidity performance"
            )

        avg_thermal_stability = features['thermal_stability_K'].mean()
        if avg_thermal_stability < 600:
            insights['recommendations'].append(
                "Prioritize MOFs with thermal stability >600K for reliable temperature-swing operation"
            )

        return insights

    def export_for_realitystream(self, output_dir: Path = None):
        """Export datasets in RealityStream-compatible format"""
        if output_dir is None:
            output_dir = self.base_path / 'realitystream_data'

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Create integrated dataset
        integrated = self.create_integrated_dataset()
        integrated_path = output_dir / 'mof-integrated-dataset.csv'
        integrated.to_csv(integrated_path, index=False)

        # Generate AI insights JSON
        features, _ = self.load_data()
        insights = self.generate_ai_insights(features)
        insights_path = output_dir / 'mof-ai-insights.json'
        with open(insights_path, 'w') as f:
            json.dump(insights, f, indent=2)

        print(f"✓ Exported integrated dataset to: {integrated_path}")
        print(f"✓ Exported AI insights to: {insights_path}")

        return integrated_path, insights_path


def main():
    """Main integration workflow"""
    print("MOF Water Capture - Data Integration Pipeline")
    print("=" * 60)

    # Initialize components
    base_path = Path(__file__).parent
    integrator = RealityStreamIntegrator(base_path)
    simulator = MOFAdsorptionSimulator()
    optimizer = HighAltitudeOptimizer()

    # Load data
    print("\n1. Loading MOF datasets...")
    features, targets = integrator.load_data()
    print(f"   ✓ Loaded {len(features)} MOF samples")
    print(f"   ✓ Features: {list(features.columns)}")

    # Simulate adsorption isotherms for first MOF
    print("\n2. Simulating adsorption isotherms...")
    sample_mof = features.iloc[0].to_dict()
    humidity_range = np.linspace(0.1, 0.9, 50)
    simulation = simulator.simulate_mof_performance(sample_mof, humidity_range)
    print(f"   ✓ Daily yield estimate: {simulation['daily_yield_L_kg_day']:.2f} L/kg/day")

    # Optimize for datacenter location
    print("\n3. Optimizing for datacenter locations...")
    location = {'altitude_m': 1200, 'humidity': 0.4, 'temp_K': 290}
    optimized_mofs = optimizer.optimize_for_location(features, location)
    print(f"   ✓ Top MOF: FIPS {optimized_mofs.iloc[0]['Fips']}")
    print(f"   ✓ Performance score: {optimized_mofs.iloc[0]['performance_score']:.3f}")

    # Export for RealityStream
    print("\n4. Exporting for RealityStream ML pipeline...")
    integrated_path, insights_path = integrator.export_for_realitystream()

    # Generate summary
    print("\n5. Integration Summary")
    print("   " + "-" * 56)
    insights = integrator.generate_ai_insights(features)
    print(f"   Dataset: {insights['dataset_info']['name']}")
    print(f"   Samples: {insights['dataset_info']['num_samples']}")
    print(f"   Features: {insights['dataset_info']['num_features']}")
    print(f"   Key findings: {len(insights['key_findings'])}")
    print(f"   Recommendations: {len(insights['recommendations'])}")

    print("\n" + "=" * 60)
    print("Integration complete! Data ready for:")
    print("  • RealityStream ML CoLab analysis")
    print("  • Team/Projects AI insights viewer")
    print("  • X.com/Grok progress sharing")
    print("=" * 60)


if __name__ == '__main__':
    main()
