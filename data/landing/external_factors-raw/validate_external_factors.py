#!/usr/bin/env python3
"""
External Factors Dataset Validation
Validates completeness of external_factors-raw for ML processing
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional

class ExternalFactorsValidator:
    def __init__(self, base_dir: str = "data/landing/external_factors-raw"):
        self.base_dir = Path(base_dir)
        self.validation_results = {}
        
    def validate_data_completeness(self) -> Dict:
        """Validate completeness of all external factor datasets"""
        print("VALIDING EXTERNAL FACTORS DATASET COMPLETENESS")
        print("=" * 60)
        
        # Define required data categories
        required_categories = {
            'economic_indicators': {
                'macro': ['ptax', 'selic', 'ipca'],
                'global': ['gdp_current_usd', 'gdp_growth_pct', 'gdp_ppp']
            },
            'commodity_prices': ['copper', 'aluminum', 'steel', 'semiconductors'],
            'market_indices': ['sp500', 'nasdaq', 'telecom_etfs', 'vix'],
            'energy_prices': ['electricity_tariffs', 'natural_gas', 'crude_oil', 'renewable_energy'],
            'climate_data': ['inmet_historical', 'openweather_current'],
            'logistics_data': ['anp_fuel', 'baltic_dry', 'freight_indices']
        }
        
        results = {
            'validation_timestamp': datetime.now().isoformat(),
            'categories': {},
            'ml_readiness': {},
            'missing_data': [],
            'recommendations': []
        }
        
        # Check each category
        for category, requirements in required_categories.items():
            category_result = self.validate_category(category, requirements)
            results['categories'][category] = category_result
        
        # Calculate ML readiness
        results['ml_readiness'] = self.calculate_ml_readiness(results['categories'])
        results['missing_data'] = self.identify_missing_data(results['categories'])
        results['recommendations'] = self.generate_recommendations(results['missing_data'])
        
        return results
    
    def validate_category(self, category: str, requirements: Dict) -> Dict:
        """Validate specific data category"""
        print(f"\nValidating {category}...")
        
        category_result = {
            'status': 'unknown',
            'completeness': 0,
            'total_required': len(requirements),
            'found_sources': [],
            'missing_sources': [],
            'data_quality': 'unknown'
        }
        
        found_count = 0
        
        for source in requirements:
            if self.check_data_source_exists(source, category):
                found_count += 1
                category_result['found_sources'].append(source)
                print(f"  ✓ {source}")
            else:
                category_result['missing_sources'].append(source)
                print(f"  ✗ {source}")
        
        category_result['completeness'] = (found_count / len(requirements)) * 100
        
        if found_count == len(requirements):
            category_result['status'] = 'complete'
            print(f"  Status: COMPLETE (100%)")
        elif found_count >= len(requirements) * 0.7:
            category_result['status'] = 'mostly_complete'
            print(f"  Status: MOSTLY COMPLETE ({category_result['completeness']:.1f}%)")
        elif found_count > 0:
            category_result['status'] = 'partial'
            print(f"  Status: PARTIAL ({category_result['completeness']:.1f}%)")
        else:
            category_result['status'] = 'missing'
            print(f"  Status: MISSING (0%)")
        
        return category_result
    
    def check_data_source_exists(self, source: str, category: str) -> bool:
        """Check if specific data source exists"""
        # Map sources to file paths
        source_mappings = {
            'ptax': 'macro/bacen/ptax/usd',
            'selic': 'macro/bacen/selic',
            'ipca': 'macro/ibge/ipca',
            'gdp_current_usd': 'global/worldbank/gdp_current_usd',
            'gdp_growth_pct': 'global/worldbank/gdp_growth_pct',
            'gdp_ppp': 'global/worldbank/gdp_ppp',
            'copper': 'commodities/*/copper_prices.csv',
            'aluminum': 'commodities/*/aluminum_prices.csv',
            'steel': 'commodities/*/steel_prices.csv',
            'semiconductors': 'commodities/*/semiconductor_index.csv',
            'sp500': 'market_indices/*/sp500.csv',
            'nasdaq': 'market_indices/*/nasdaq.csv',
            'telecom_etfs': 'market_indices/*/telecom_etfs.csv',
            'vix': 'market_indices/*/vix.csv',
            'electricity_tariffs': 'energy/*/electricity_tariffs.csv',
            'natural_gas': 'energy/*/natural_gas_prices.csv',
            'crude_oil': 'energy/*/crude_oil_prices.csv',
            'renewable_energy': 'energy/*/renewable_energy.csv',
            'inmet_historical': 'inmet/202*/INMET_*.CSV',
            'openweather_current': 'openweather/*/brazil_weather_expanded.csv',
            'anp_fuel': 'logistics/anp_fuel/*/anp_fuel.csv',
            'baltic_dry': 'logistics/baltic_dry/*/baltic_dry.csv',
            'freight_indices': 'logistics/freight/*/air_freight_mtkm.csv'
        }
        
        pattern = source_mappings.get(source, '')
        if not pattern:
            return False
        
        # Check if files exist matching pattern
        search_path = self.base_dir / pattern
        try:
            if search_path.exists():
                if '*' in str(search_path):
                    # Check for any files matching the pattern
                    parent_dir = search_path.parent
                    glob_pattern = search_path.name
                    import glob
                    matches = glob.glob(str(parent_dir / glob_pattern))
                    return len(matches) > 0
                else:
                    return search_path.exists() and search_path.stat().st_size > 0
        except Exception:
            return False
        
        return False
    
    def calculate_ml_readiness(self, category_results: Dict) -> Dict:
        """Calculate ML pipeline readiness"""
        critical_categories = ['economic_indicators', 'commodity_prices', 'market_indices', 'climate_data']
        important_categories = ['energy_prices', 'logistics_data']
        
        critical_complete = sum(1 for cat in critical_categories 
                           if category_results.get(cat, {}).get('status') == 'complete')
        critical_partial = sum(1 for cat in critical_categories 
                           if category_results.get(cat, {}).get('status') in ['mostly_complete', 'partial'])
        
        important_complete = sum(1 for cat in important_categories 
                             if category_results.get(cat, {}).get('status') == 'complete')
        important_partial = sum(1 for cat in important_categories 
                             if category_results.get(cat, {}).get('status') in ['mostly_complete', 'partial'])
        
        total_critical = len(critical_categories)
        total_important = len(important_categories)
        
        # Calculate readiness percentage
        critical_score = (critical_complete * 100 + critical_partial * 50) / total_critical
        important_score = (important_complete * 100 + important_partial * 25) / total_important
        overall_score = (critical_score + important_score) / 2
        
        if overall_score >= 90:
            readiness = 'READY'
        elif overall_score >= 70:
            readiness = 'MOSTLY_READY'
        elif overall_score >= 50:
            readiness = 'PARTIALLY_READY'
        else:
            readiness = 'NOT_READY'
        
        return {
            'overall_score': overall_score,
            'readiness_level': readiness,
            'critical_complete': critical_complete,
            'total_critical': total_critical,
            'important_complete': important_complete,
            'total_important': total_important
        }
    
    def identify_missing_data(self, category_results: Dict) -> List[str]:
        """Identify missing critical data sources"""
        missing = []
        
        for category, result in category_results.items():
            if result['status'] in ['missing', 'partial']:
                for source in result['missing_sources']:
                    missing.append(f"{category}:{source}")
        
        return missing
    
    def generate_recommendations(self, missing_data: List[str]) -> List[str]:
        """Generate recommendations for missing data"""
        recommendations = []
        
        if not missing_data:
            recommendations.append("Dataset is complete for ML processing")
            return recommendations
        
        # Category-specific recommendations
        missing_categories = set(item.split(':')[0] for item in missing_data)
        
        if 'economic_indicators' in missing_categories:
            recommendations.append("Run macro data fetchers: python scripts/etl/external/fetch_macro.py")
        
        if 'commodity_prices' in missing_categories:
            recommendations.append("Download commodity data: python commodities_downloader.py")
        
        if 'market_indices' in missing_categories:
            recommendations.append("Fetch market indices: python market_indices_downloader.py")
        
        if 'energy_prices' in missing_categories:
            recommendations.append("Get energy data: python energy_downloader.py")
        
        if 'climate_data' in missing_categories:
            recommendations.append("Expand weather coverage: python brazil_weather_fetcher.py")
        
        if 'logistics_data' in missing_categories:
            recommendations.append("Update freight data: check logistics/downloaders")
        
        # General recommendations
        recommendations.append("Run complete orchestrator: python complete_external_downloader.py")
        recommendations.append("Validate transformation scripts: check scripts/etl/transform/")
        recommendations.append("Test ML pipeline integration: python scripts/validation/test_ml_ready.py")
        
        return recommendations
    
    def generate_report(self, results: Dict) -> str:
        """Generate validation report"""
        report = []
        report.append("# EXTERNAL FACTORS DATASET VALIDATION REPORT")
        report.append(f"Generated: {results['validation_timestamp']}")
        report.append("")
        
        # Executive Summary
        report.append("## EXECUTIVE SUMMARY")
        readiness = results['ml_readiness']
        report.append(f"ML Readiness Level: {readiness['readiness_level']}")
        report.append(f"Overall Score: {readiness['overall_score']:.1f}/100")
        report.append(f"Critical Categories: {readiness['critical_complete']}/{readiness['total_critical']} complete")
        report.append(f"Important Categories: {readiness['important_complete']}/{readiness['total_important']} complete")
        report.append("")
        
        # Category Details
        report.append("## CATEGORY DETAILS")
        for category, result in results['categories'].items():
                    status_emoji = {
                'complete': '+',
                'mostly_complete': '~',
                'partial': '-',
                'missing': 'x'
            }.get(result['status'], '?')
            
            report.append(f"### {category.replace('_', ' ').title()}")
            report.append(f"Status: {status_emoji} {result['status'].upper()}")
            report.append(f"Completeness: {result['completeness']:.1f}%")
            
            if result['found_sources']:
                report.append(f"Found: {', '.join(result['found_sources'])}")
            
            if result['missing_sources']:
                report.append(f"Missing: {', '.join(result['missing_sources'])}")
            
            report.append("")
        
        # Missing Data
        if results['missing_data']:
            report.append("## MISSING CRITICAL DATA")
            for item in results['missing_data']:
                report.append(f"- {item}")
            report.append("")
        
        # Recommendations
        report.append("## RECOMMENDATIONS")
        for i, rec in enumerate(results['recommendations'], 1):
            report.append(f"{i}. {rec}")
        report.append("")
        
        # Next Steps
        report.append("## NEXT STEPS")
        report.append("1. Address missing data sources using the downloaders above")
        report.append("2. Run data transformation to silver layer")
        report.append("3. Validate ML pipeline integration")
        report.append("4. Set up automated data refresh schedule")
        report.append("")
        
        return "\n".join(report)
    
    def save_report(self, report: str, results: Dict):
        """Save validation report and results"""
        # Save text report
        report_file = self.base_dir / 'validation_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nValidation report saved to: {report_file}")
        
        # Save JSON results
        json_file = self.base_dir / 'validation_results.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Detailed results saved to: {json_file}")

def main():
    """Main execution function"""
    validator = ExternalFactorsValidator()
    
    # Run validation
    results = validator.validate_data_completeness()
    
    # Generate and save report
    report = validator.generate_report(results)
    validator.save_report(report, results)
    
    print("\n" + "=" * 60)
    print("EXTERNAL FACTORS VALIDATION COMPLETED")
    print("=" * 60)
    
    return results, report

if __name__ == "__main__":
    main()