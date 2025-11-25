import argparse
import os
import duckdb
from loguru import logger
import configparser
import sys
import smtplib
from email.message import EmailMessage

parser = argparse.ArgumentParser(description="Temperature Average Calculator")
parser.add_argument("--config", required=True, help="Path to config INI file")
parser.add_argument("--env", required=True, choices=["qa", "prod"], help="Environment (qa or prod)")
parser.add_argument("--format", required=True, choices=["csv", "parquet"], help="File format (csv or parquet)")
args = parser.parse_args()

logger.add("app.log", rotation="1 MB")


config = configparser.ConfigParser()

try:
    config.read(args.config)
    input_path = config[args.env]["input_path"]
    output_path = config[args.env]["output_path"]
    input_file = config[args.env]["input_file"]
    output_file = config[args.env]["output_file"]
except Exception as e:
    logger.error(f"Error reading config file: {e}")
    sys.exit(1)

input_file_path = os.path.join(input_path, input_file)
output_file_path = os.path.join(output_path, output_file)

logger.info(f"Environment: {args.env.upper()}")
logger.info(f"File format: {args.format}")
logger.info(f"Input file path: {input_file_path}")

try:
    con = duckdb.connect()

    if args.format == "csv":
        df = con.execute(f"""
            SELECT Country, State, AVG(AvgTemperature) AS AvgTemperature
            FROM read_csv_auto('{input_file_path}')
            GROUP BY Country, State
        """).df()
    else:
        df = con.execute(f"""
            SELECT Country, State, AVG(AvgTemperature) AS AvgTemperature
            FROM read_parquet('{input_file_path}')
            GROUP BY Country, State
        """).df()

    logger.info("Average temperature calculated successfully using DuckDB.")

except Exception as e:
    logger.error(f"DuckDB transformation error: {e}")
    sys.exit(1)


try:
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
        logger.warning("Old output file deleted.")

    os.makedirs(output_path, exist_ok=True)

    if args.format == "csv":
        df.to_csv(output_file_path, index=False)
    else:
        df.to_parquet(output_file_path, index=False)

    logger.info(f"Output saved successfully at: {output_file_path}")

except Exception as e:
    logger.error(f"Error saving output: {e}")
    sys.exit(1)


try:
    smtp_server = config["email"]["smtp_server"]
    smtp_port = int(config["email"]["smtp_port"])
    sender = config["email"]["sender"]
    password = config["email"]["password"]
    receiver = config["email"]["receiver"]

    msg = EmailMessage()
    msg["Subject"] = "Temperature Processing Result"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Please find the processed temperature file attached.")

    with open(output_file_path, "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream",
                       filename=os.path.basename(output_file_path))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

    logger.info("Email sent successfully.")

except Exception as e:
    logger.error(f"Error sending email: {e}")
    sys.exit(1)

print("Task Completed Successfully!")
