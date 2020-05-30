from django import template  
import datetime  
from cryptography.fernet import Fernet
register = template.Library()    

@register.filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    seconds, micros = divmod(int(timestamp), 1000000)
    days, seconds = divmod(seconds, 86400)
    date = datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, micros)
    return date.strftime('%a, %d %B %Y %H:%M:%S %Z')
    # print(date.strftime('%a, %d %B %Y %H:%M:%S %Z'))