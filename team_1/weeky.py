import calendar
from datetime import datetime, timedelta

def week_of_month(time : datetime):
    """
    월요일을 기준으로 한 달의 몇 주차인지 계산하는 함수
    """
    DT = time
    year, month, day = DT.year, DT.month, DT.day
    first_day_weekday, num_days = calendar.monthrange(year, month)
    offset = (7 - first_day_weekday) % 7
    if day <= offset:
        return 1
    else:
        return (day - offset - 1) // 7 + 2
    


