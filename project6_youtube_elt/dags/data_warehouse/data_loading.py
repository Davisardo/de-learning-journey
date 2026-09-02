import json
from datetime import date
import logging


logger = logging.getLogger(__name__)


def load_data():
    file_path = f"./data/youtube_data_{date.today()}.json"
    try:
        logger.info(f"Processing file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON data: {file_path}")
        raise
