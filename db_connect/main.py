from sqlalchemy import create_engine,text
from loguru import logger
import pandas as pd
from create_db import create_db

logger.add("app.log", rotation="1 MB")

def fetch_data():
    try:
        logger.info("Starting the process...")
        create_db()
        logger.info("Connecting to database to fetch data...")
        engine=create_engine(f"sqlite:///task.db")

        with engine.connect() as conn:
            result=conn.execute(text("SELECT * from employees"))
            logger.info(f"Fetching data from the database")
            df=pd.DataFrame(result.fetchall(),columns=result.keys())
            logger.info("Loaded data to Dataframe")
            df.to_csv("employee.csv",index=False)
            logger.info(f"Data saved to csv file")
    except Exception as e:
        logger.error(f"Error in fetching and saving data : {e}")
        raise

if __name__ =="__main__":
    fetch_data()

