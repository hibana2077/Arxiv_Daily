import datetime
now = datetime.datetime.now()
print(now.strftime('%H:%M') >= '09:00')