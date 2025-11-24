import argparse
from extractor import process_json

parser = argparse.ArgumentParser(description="Universal JSON Flattener (Loguru Version)")
parser.add_argument("--config", required=True, help="Path to config.ini")

args = parser.parse_args()

df = process_json(args.config)
print(df)
