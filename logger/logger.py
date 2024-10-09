import logging
from inventory_management.settings import LOGGING_FILENAME, LOGGING_DIRECTORY
logging.basicConfig(
    filename=f"{LOGGING_DIRECTORY}/{LOGGING_FILENAME}",
    filemode="a",
    level="INFO",
    format="%(asctime)s - %(filename)s:%(lineno)d [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()