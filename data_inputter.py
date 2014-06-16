import datetime

today = raw_input("Are you entering data for today? [Y/n] ")

def now(opt):
    return str(datetime.date.today().strftime(opt))

def get_date():
    year = raw_input("Year? [{}] ".format(now("%Y")))
    month = raw_input("Month? [{}] ".format(now("%m")))
    day = raw_input("Date? [{}] ".format(now("%d")))
    if year == "":
        year = now("%Y")
    if month == "":
        month = now("%m")
    if day == "":
        day = now("%d")
    return "{year}-{month}-{day}".format(year=year, month=month, day=day)

if (today == "") or (today == "y"):
    date = datetime.date.today()
else:
    date = get_date()

with open('push_up_data.csv', 'a') as f:
    f.write("{date}\n".format(date=str(date)))

