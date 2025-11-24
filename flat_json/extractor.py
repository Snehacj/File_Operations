import json
import pandas as pd
import configparser
import os
from loguru import logger
from collections.abc import MutableMapping


def setup_logger(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger.remove() 
    logger.add(log_file, rotation="1 MB", level="INFO")  
    logger.add(lambda msg: print(msg, end=""))


def load_config(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    config = configparser.ConfigParser()
    config.read(path)

    return {
        "input_file": config["FILES"].get("input_file"),
        "output_file": config["FILES"].get("output_file"),
        "log_file": config["FILES"].get("log_file", "logs/app.log"),
        "extract_all": config["OPTIONS"].getboolean("extract_all", True),
        "filters": [
            f.strip()
            for f in config["OPTIONS"].get("filters", "").split(",")
            if f.strip()
        ]
    }


def safe_read_json(path):
    if not os.path.exists(path):
        logger.error(f"JSON file not found: {path}")
        raise FileNotFoundError(f"JSON file not found: {path}")

    try:
        with open(path, 'r') as f:
            data = json.load(f)
            logger.info(f"Loaded JSON from {path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error while reading JSON: {e}")
        raise


def flatten_json(data, parent_key="", sep="."):
    items = []

    if isinstance(data, MutableMapping):
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            items.extend(flatten_json(value, new_key, sep=sep).items())

    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_key = f"{parent_key}{sep}{index}" if parent_key else str(index)
            items.extend(flatten_json(value, new_key, sep=sep).items())

    else:
        return {parent_key: data}

    return dict(items)


def apply_filters(flattened_json: dict, extract_all: bool, filters: list):
    if extract_all:
        return flattened_json

    filtered = {}
    for key, value in flattened_json.items():
        if any(f.lower() in key.lower() for f in filters):
            filtered[key] = value

    return filtered


def process_json(config_path: str) -> pd.DataFrame:
    cfg = load_config(config_path)
    setup_logger(cfg["log_file"])

    logger.info("Starting JSON flattening process")

    json_data = safe_read_json(cfg["input_file"])

    if isinstance(json_data, dict):
        json_data = [json_data]

    processed = []
    for record in json_data:
        try:
            flat = flatten_json(record)
            filtered = apply_filters(flat, cfg["extract_all"], cfg["filters"])
            processed.append(filtered)
        except Exception as e:
            logger.exception(f"Failed processing JSON record: {e}")

    df = pd.DataFrame(processed)

    try:
        df.to_csv(cfg["output_file"], index=False)
        logger.info(f"Saved output CSV → {cfg['output_file']}")
    except Exception as e:
        logger.error(f"Failed to save output CSV: {e}")
        raise

    return df
