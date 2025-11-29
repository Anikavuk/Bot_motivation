from prediction_app.core.config_run import run_app
from prediction_app.core.logger import get_logger

logger = get_logger(name=__name__)


def start() -> None:
    logger.info("Starting...")
    run_app()
    logger.info("Stopping...")
