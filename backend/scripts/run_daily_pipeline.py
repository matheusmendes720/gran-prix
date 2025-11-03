#!/usr/bin/env python3
"""
Daily pipeline runner for Nova Corrente
Runs automated daily collection and feature calculation
"""
import sys
from pathlib import Path
from datetime import date

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.integration_service import integration_service
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.scripts.daily_pipeline')


def main():
    """Run daily pipeline"""
    try:
        logger.info("Starting daily pipeline")
        
        # Run daily pipeline
        result = integration_service.run_daily_pipeline()
        
        # Print results
        print(f"Daily Pipeline Results:")
        print(f"  Status: {result['status']}")
        print(f"  Date: {result['date']}")
        print(f"  External Data: {result['external_data']}")
        print(f"  Aggregations: {result['aggregations']}")
        print(f"  Features Calculated: {result['features_calculated']}")
        print(f"  Insights Generated: {result['insights_generated']}")
        
        if result['errors']:
            print(f"  Errors: {len(result['errors'])}")
            for error in result['errors']:
                print(f"    - {error}")
        
        logger.info(f"Daily pipeline completed: {result['status']}")
        
        # Exit with error code if there were errors
        if result['errors']:
            sys.exit(1)
        
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in daily pipeline: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()


