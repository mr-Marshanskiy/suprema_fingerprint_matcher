from datetime import datetime


def get_now():
    return datetime.now()


def get_today():
    return datetime.now().date()


def format_time(value, format='%H:%M'):
    try:
        return value.strftime(format)
    except:
        return value


def concat_date_and_time(date_value, time_value):
    result = datetime(date_value.year,
                      date_value.month,
                      date_value.day,
                      time_value.hour,
                      time_value.minute,
                      time_value.second)
    return result
