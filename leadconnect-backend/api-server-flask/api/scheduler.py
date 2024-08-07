# scheduler.py
import schedule
import time
import requests
from datetime import datetime
from pytz import timezone
from threading import Thread

def hit_api():
    url = "http://127.0.0.1:5000/api/users/notifications" 
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        # Your payload data
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("API call successful.")
    else:
        print(f"API call failed with status code: {response.status_code}")
        print(response.json())

def job():
    est = timezone('US/Eastern')
    now = datetime.now(est)
    print(f"Running job at {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    hit_api()

def run_scheduler():
    schedule.every().day.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
