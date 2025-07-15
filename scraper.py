import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

URL = "https://www.adr.it/fiumicino"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ADRScraper/1.0)"}

def extract_wait_times():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    text = BeautifulSoup(response.text, "html.parser").get_text()

    minutes = re.findall(r"(\d+)\s*min", text)
    if len(minutes) < 2:
        raise ValueError(f"Expected at least 2 wait times, found: {minutes}")

    labels = ["Terminal 1", "Terminal 3"]
    wait_times = {label: int(minutes[i]) for i, label in enumerate(labels)}
    return wait_times

def write_to_csv(wait_times: dict, file_path="wait_times.csv"):
    file_exists = os.path.isfile(file_path)
    now = datetime.utcnow().isoformat()

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "Terminal 1 (min)", "Terminal 3 (min)"])
        writer.writerow([now, wait_times["Terminal 1"], wait_times["Terminal 3"]])

if __name__ == "__main__":
    try:
        wait_times = extract_wait_times()
        write_to_csv(wait_times)
        logging.info(f"✅ Scraped at {datetime.utcnow()} → {wait_times}")
    except Exception as e:
        logging.error(f"❌ Error: {e}")