import asyncio

from app.core.config_run import run_app
from app.core.logger import Logger
from app.core.time_based_deletion import checking_time

logger_factory = Logger(mode="dev")
logger = logger_factory.get_logger(__name__)


if __name__ == "__main__":
    logger.info("Starting...")
    asyncio.run(checking_time())
    run_app()
    logger.info("Stopping...")
