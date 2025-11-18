"""
Orchestrator service for Nova Corrente
Coordinates all ETL pipelines and feature engineering
"""
from typing import Dict, Any, Optional, List
from datetime import date, datetime, timedelta
import time
import threading

# Optional: schedule library for automated jobs
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    schedule = None

from backend.services.integration_service import integration_service
from backend.pipelines.climate_etl import climate_etl
from backend.pipelines.economic_etl import economic_etl
from backend.pipelines.anatel_5g_etl import anatel_5g_etl
from backend.pipelines.brazilian_calendar_etl import brazilian_calendar_etl
from backend.pipelines.feature_calculation_etl import feature_calculation_etl
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.pipelines.orchestrator')


class OrchestratorService:
    """
    Orchestrator for all ETL pipelines and automated jobs
    """
    
    def __init__(self):
        """Initialize orchestrator"""
        self.running = False
        self.scheduler_thread = None
    
    def run_complete_pipeline(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Run complete ETL pipeline for all data sources
        
        Args:
            start_date: Start date (default: 30 days ago)
            end_date: End date (default: today)
        
        Returns:
            Dictionary with pipeline execution results
        """
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        
        if end_date is None:
            end_date = date.today()
        
        results = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'pipelines': {},
            'status': 'success',
            'errors': []
        }
        
        try:
            logger.info(f"Starting complete pipeline from {start_date} to {end_date}")
            
            # 1. Generate Brazilian calendar if needed
            try:
                year_start = start_date.year
                year_end = end_date.year
                rows = brazilian_calendar_etl.run(year_start, year_end)
                results['pipelines']['calendar'] = {'rows': rows, 'status': 'success'}
            except Exception as e:
                logger.error(f"Error in calendar ETL: {e}")
                results['pipelines']['calendar'] = {'status': 'error', 'error': str(e)}
                results['errors'].append(f"Calendar: {str(e)}")
            
            # 2. Climate data
            try:
                rows = climate_etl.run(start_date, end_date)
                results['pipelines']['climate'] = {'rows': rows, 'status': 'success'}
            except Exception as e:
                logger.error(f"Error in climate ETL: {e}")
                results['pipelines']['climate'] = {'status': 'error', 'error': str(e)}
                results['errors'].append(f"Climate: {str(e)}")
            
            # 3. Economic data
            try:
                rows = economic_etl.run(start_date, end_date)
                results['pipelines']['economic'] = {'rows': rows, 'status': 'success'}
            except Exception as e:
                logger.error(f"Error in economic ETL: {e}")
                results['pipelines']['economic'] = {'status': 'error', 'error': str(e)}
                results['errors'].append(f"Economic: {str(e)}")
            
            # 4. 5G data
            try:
                rows = anatel_5g_etl.run(start_date, end_date)
                results['pipelines']['5g'] = {'rows': rows, 'status': 'success'}
            except Exception as e:
                logger.error(f"Error in 5G ETL: {e}")
                results['pipelines']['5g'] = {'status': 'error', 'error': str(e)}
                results['errors'].append(f"5G: {str(e)}")
            
            # 5. Calculate features for all materials
            try:
                count = feature_calculation_etl.run(
                    date_ref=end_date,
                    material_ids=None  # All materials
                )
                results['pipelines']['features'] = {'count': count, 'status': 'success'}
            except Exception as e:
                logger.error(f"Error in feature calculation: {e}")
                results['pipelines']['features'] = {'status': 'error', 'error': str(e)}
                results['errors'].append(f"Features: {str(e)}")
            
            # Expanded pipelines would be added here:
            # - Transport ETL
            # - Trade ETL
            # - Energy ETL
            # - Employment ETL
            # - Construction ETL
            # - Industrial ETL
            # - Logistics ETL
            # - Regional ETL
            
            if results['errors']:
                results['status'] = 'partial_success'
            else:
                results['status'] = 'success'
            
            logger.info(
                f"Complete pipeline finished: {len(results['pipelines'])} pipelines, "
                f"{len(results['errors'])} errors"
            )
            
            return results
        except Exception as e:
            logger.error(f"Error in complete pipeline: {e}")
            results['status'] = 'error'
            results['errors'].append(f"Pipeline: {str(e)}")
            return results
    
    def schedule_daily_job(self, time_str: str = "02:00"):
        """
        Schedule daily pipeline job
        
        Args:
            time_str: Time to run daily job (default: 02:00)
        """
        try:
            if not SCHEDULE_AVAILABLE:
                logger.warning("schedule library not available. Install with: pip install schedule")
                return
            
            schedule.clear()
            schedule.every().day.at(time_str).do(self._run_daily_job)
            logger.info(f"Scheduled daily job at {time_str}")
        except Exception as e:
            logger.error(f"Error scheduling daily job: {e}")
            raise
    
    def _run_daily_job(self):
        """Run daily job"""
        try:
            logger.info("Running scheduled daily job")
            result = integration_service.run_daily_pipeline()
            logger.info(f"Daily job completed: {result['status']}")
        except Exception as e:
            logger.error(f"Error in daily job: {e}")
    
    def start_scheduler(self, time_str: str = "02:00"):
        """
        Start scheduler thread
        
        Args:
            time_str: Time to run daily job
        """
        try:
            if not SCHEDULE_AVAILABLE:
                logger.warning("schedule library not available. Install with: pip install schedule")
                return
            
            if self.running:
                logger.warning("Scheduler already running")
                return
            
            self.schedule_daily_job(time_str)
            self.running = True
            
            def run_scheduler():
                while self.running:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
            
            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            self.scheduler_thread.start()
            
            logger.info("Scheduler started")
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            raise
    
    def stop_scheduler(self):
        """Stop scheduler thread"""
        try:
            self.running = False
            if SCHEDULE_AVAILABLE:
                schedule.clear()
            if self.scheduler_thread:
                self.scheduler_thread.join(timeout=5)
            logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")


# Singleton instance
orchestrator_service = OrchestratorService()

