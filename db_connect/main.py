from sqlalchemy import create_engine,text
from loguru import logger
import pandas as pd
from create_db import create_db
import json
import duckdb

logger.add("app.log", rotation="1 MB")

def fetch_data():
    try:
        logger.info("Starting the process...")
        with open("config.json","r") as f:
            config=json.load(f)
        query=config["query"]
        output_file=config["output"]
        ddb=config["duckdb_query"]


        create_db()
        logger.info("Connecting to database to fetch data...")
        engine=create_engine(f"sqlite:///task.db")

        with engine.connect() as conn:
            result=conn.execute(text(query))
            logger.info(f"Fetching data from the database")
            df=pd.DataFrame(result.fetchall(),columns=result.keys())
            logger.info("Loaded data to Dataframe")

            dresult=duckdb.query(ddb).df()
            logger.info(f"Executing duckdb query...")

            dresult.to_csv(output_file,index=False)
            logger.info(f"Data saved to csv file")

    except Exception as e:
        logger.error(f"Error in fetching and saving data : {e}")
        raise

if __name__ =="__main__":
    fetch_data()

