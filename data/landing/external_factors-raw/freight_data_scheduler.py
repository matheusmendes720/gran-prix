"""
Scheduling script for automated daily/weekly downloads
Requires: pip install schedule APScheduler
"""

import schedule
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FreightDataScheduler:
    def __init__(self):
        self.schedule = schedule.Scheduler()

    def run_bdi_download(self):
        """Run BDI download via Trading Economics"""
        logger.info("Starting BDI download...")
        try:
            from trading_econ_fetcher import TradingEconomicsFreightFetcher
            fetcher = TradingEconomicsFreightFetcher()
            data = fetcher.get_historical_ticker('BDIY')
            if data:
                fetcher.save_to_csv(data, f"data/manual/bdi_{datetime.now().strftime('%Y%m%d')}.csv")
                logger.info("✓ BDI download completed")
        except Exception as e:
            logger.error(f"BDI download failed: {e}")

    def run_imf_download(self):
        """Run IMF Shipping Cost Index download"""
        logger.info("Starting IMF SCI download...")
        try:
            from worldbank_freight_fetcher import WorldBankFreightFetcher
            fetcher = WorldBankFreightFetcher()
            data = fetcher.get_indicator('IM.fs.sp_cons.sh')
            if data:
                fetcher.save_csv(data, f"data/manual/imf_sci_{datetime.now().strftime('%Y%m%d')}.csv")
                logger.info("✓ IMF SCI download completed")
        except Exception as e:
            logger.error(f"IMF download failed: {e}")

    def setup_daily_schedule(self):
        """Setup daily download tasks"""
        # Daily at 2 AM
        self.schedule.every().day.at("02:00").do(self.run_bdi_download)

        # Weekly on Monday at 3 AM (Drewry publishes weekly)
        self.schedule.every().monday.at("03:00").do(self.run_imf_download)

        logger.info("Schedule configured")

    def run_continuous(self):
        """Run scheduler in continuous loop"""
        logger.info("Scheduler started. Press Ctrl+C to stop.")

        while True:
            self.schedule.run_pending()
            time.sleep(60)

# Alternative: APScheduler for production use
def setup_apscheduler():
    """Setup with APScheduler for production (background service)"""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger

        scheduler = BackgroundScheduler()

        # BDI daily at 2 AM
        scheduler.add_job(
            FreightDataScheduler().run_bdi_download,
            CronTrigger(hour=2, minute=0),
            id='bdi_daily'
        )

        # IMF weekly Monday 3 AM
        scheduler.add_job(
            FreightDataScheduler().run_imf_download,
            CronTrigger(day_of_week='mon', hour=3, minute=0),
            id='imf_weekly'
        )

        scheduler.start()
        logger.info("APScheduler started in background")
        return scheduler

    except ImportError:
        logger.warning("APScheduler not installed")
        return None

# Usage examples
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['once', 'schedule', 'apscheduler'], 
                       default='once',
                       help='Run mode: single execution, schedule loop, or background')
    args = parser.parse_args()

    scheduler = FreightDataScheduler()

    if args.mode == 'once':
        scheduler.run_bdi_download()
        scheduler.run_imf_download()

    elif args.mode == 'schedule':
        scheduler.setup_daily_schedule()
        scheduler.run_continuous()

    elif args.mode == 'apscheduler':
        setup_apscheduler()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
