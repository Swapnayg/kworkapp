from datetime import datetime, timedelta,date
from dateutil import relativedelta
today = datetime.today()
first = today.replace(day=1)
last_date = first - timedelta(days=1)
end_date = datetime.strptime(last_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
start_date = end_date -  relativedelta.relativedelta(months=int(3))
print(end_date)
print(start_date)
