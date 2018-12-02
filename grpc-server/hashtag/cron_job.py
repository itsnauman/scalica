import schedule
import time

def job():
    print("I'm working...")

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
