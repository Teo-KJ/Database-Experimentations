import schedule
import time
from functions import *

schedule.every().day.at("10:30").do(insertIntoDB)
#schedule.every(10).seconds.do(insertIntoDB)

while 1:
    schedule.run_pending()
    time.sleep(1)