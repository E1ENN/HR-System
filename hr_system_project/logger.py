import logging

logging.basicConfig(
    filename='hr_system_project/errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger()