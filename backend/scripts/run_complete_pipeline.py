#!/usr/bin/env python3
"""
Complete pipeline runner for Nova Corrente
Runs complete ETL pipeline for all data sources
"""
import sys
from pathlib import Path
from datetime import date, timedelta

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.pipelines.orchestrator_service import orchestrator_service
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.scripts.complete_pipeline')


def main():
    """Run complete pipeline"""
    try:
        logger.info("Starting complete pipeline")
        
        # Default: last 30 days to today
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        # Run complete pipeline
        result = orchestrator_service.run_complete_pipeline(start_date, end_date)
        
        # Print results
        print(f"Complete Pipeline Results:")
        print(f"  Status: {result['status']}")
        print(f"  Date Range: {result['start_date']} to {result['end_date']}")
        print(f"  Pipelines: {len(result['pipelines'])}")
        
        for pipeline_name, pipeline_result in result['pipelines'].items():
            status = pipeline_result.get('status', 'unknown')
            if 'rows' in pipeline_result:
                print(f"    {pipeline_name}: {status} ({pipeline_result['rows']} rows)")
            elif 'count' in pipeline_result:
                print(f"    {pipeline_name}: {status} ({pipeline_result['count']} materials)")
            else:
                print(f"    {pipeline_name}: {status}")
            
            if 'error' in pipeline_result:
                print(f"      Error: {pipeline_result['error']}")
        
        if result['errors']:
            print(f"  Errors: {len(result['errors'])}")
            for error in result['errors']:
                print(f"    - {error}")
        
        logger.info(f"Complete pipeline finished: {result['status']}")
        
        # Exit with error code if there were errors
        if result['errors']:
            sys.exit(1)
        
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in complete pipeline: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()


