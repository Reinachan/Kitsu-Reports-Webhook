import time
from dotenv import load_dotenv
from lib.report import fetch_reports

if __name__ == "__main__":
    load_dotenv()
    while True:
        print("fetching")
        fetch_reports()
        print("fetched")
        time.sleep(60)
