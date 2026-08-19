from pathlib import Path
import logging

#creating Logs directory if doesn't already exist
Path("Logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    filename="Logs/streamly.log",
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    filemode="a"
    )