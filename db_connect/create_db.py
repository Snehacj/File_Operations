from sqlalchemy import create_engine,text
from loguru import logger

logger.add("app.log", rotation="1 MB")

def create_db():
    try:
        logger.info("Connecting to SQLite database")
        engine=create_engine("sqlite:///task.db")
        logger.info(f"Engine connected")
        with engine.begin() as conn:
            conn.execute(text(""" CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT,department TEXT,salary INTEGER) """))
            logger.info(f"Creating a table...")
            conn.execute(text(""" INSERT INTO employees (name,department,salary) 
                    VALUES(:name,:dept,:salary)"""),
                            [
                                {"name":"Ananya","dept":"IT","salary":50000},
                                {"name":"Sneha","dept":"HR","salary":40000},
                                {"name":"Anoop","dept":"Finance","salary":55000}, 
                                
                            ])
            logger.info(f"Created a table and Inserted the values successfully !!!")
    except Exception as e:
        logger.error(f"Error creating database : {e}")

