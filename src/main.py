from src.app.core.config_run import run_app
from src.app.core.logger import get_logger

logger = get_logger(name=__name__)


if __name__ == "__main__":
    logger.info("Starting...")
    run_app()
    logger.info("Stopping...")
