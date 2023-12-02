import datetime
import pytz

def format_date(date_string):
    date_format = '%a, %d %b %Y %H:%M:%S GMT'

    date = datetime.datetime.strptime(date_string, date_format)
    date = date.replace(tzinfo=pytz.utc)
    date = date.astimezone(pytz.timezone('America/Sao_Paulo'))

    new_date = date.strftime('%d-%m-%Y %H:%M:%S')

    return new_date
