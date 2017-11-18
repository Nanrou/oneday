import re
from datetime import datetime, timedelta

from scrape_util import calculate_datetime, get_data_from_redis


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


def that_day(date_string):
    if isinstance(date_string, datetime):
        date_string = '{}-{}-{}'.format(*[str(x) for x in [date_string.year, date_string.month, date_string.day]])
    elif not re.match('\d{4}-\d{1,2}-\d{1,2}', date_string):
        _now = datetime.now()
        date_string = '{}-{}-{}'.format(*[str(x) for x in [_now.year, _now.month, _now.day]])
    _p, _r = calculate_datetime(date_string)
    _data = get_data_from_redis(date_string)[0].rsplit('[')[0]
    return {'today': date_string, 'passed_day': _p, 'remain_day': _r, 'data': _data}


def another_day(date_string, opt):
    _date = datetime(*[int(x) for x in date_string.split('-')])
    if opt == 'next':
        return that_day(_date + timedelta(days=1))
    else:
        return that_day(_date - timedelta(days=1))


def today():
    _today = datetime.now()
    return that_day('{}-{}-{}'.format(_today.year, _today.month, _today.day))

