import os
import time
from datetime import datetime,timedelta
from loguru import logger

def timing(func):
    def wrapper(*args,**kwargs):
        start=datetime.now()
        logger.info(f"started at {start}")
        result=func(*args,**kwargs)
        end=datetime.now()
        logger.info(f"Ended at {end}")
        return result
    return wrapper

@timing
def file_watcher(file_path,hours,interval):
    logger.info(f"watching for {file_path}")
    end=datetime.now()+timedelta(hours=hours)
    file_ok=False

    while datetime.now() < end:
        if os.path.exists(file_path):
            modified=datetime.fromtimestamp(os.path.getmtime(file_path))
            hours_diff=(datetime.now()- modified).total_seconds()/3600
            logger.info(f"File Exists. Last modified at {modified}")

            if hours_diff <= hours:
                logger.success("File found and updated within allowed time range")
                file_ok=True
                break
            else:
                logger.warning("File exist but not updated recently")

        else:
            logger.warning("File not found !!!")

        time.sleep(interval)


    if not file_ok:
        logger.error("Failed: File not found or not updated in the last N hours")
        raise FileNotFoundError("File not available or not updated in allowed time.")
    
    logger.success("File meets criteria.Processing file now...")

 