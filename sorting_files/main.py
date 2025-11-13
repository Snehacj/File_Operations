import argparse
import configparser
from script import Sorting
from loguru import logger

def main():
    parser=argparse.ArgumentParser(description="Sorting files by extension")
    parser.add_argument("source")
    parser.add_argument("config")
    parser.add_argument("destination")
    args=parser.parse_args()

    config=configparser.ConfigParser()
    config.read(args.config)

    if "CATEGORIES" not in config:
        logger.error(f"issing [CATEGORIES] in config.ini")
        return
    
    sorter=Sorting()
    sorter.sort_files(args.source,args.destination,config["CATEGORIES"])


if __name__ =="__main__":
    main()