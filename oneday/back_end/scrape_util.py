from random import sample
from datetime import datetime, timedelta
import re

import requests
from bs4 import BeautifulSoup
from redis import ConnectionPool, Redis


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
WIKI_HOME_URI = 'https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5'
SINGLE_DAY_URI = 'https://zh.wikipedia.org/zh-cn/{month}月{day}日'  # 格式为：11月16日


def download_page(uri):
    resp = requests.get(uri, headers=HEADER)
    return resp.text


def scrape_home(rf):
    soup = BeautifulSoup(rf, 'lxml')
    div = soup.find(id='mp-2012-column-otd-block').find(id='column-otd')
    date = div.p.span.string
    dts = []
    for item in div.dl.find_all('dt'):
        dts.append(item.a.string)
    dds = []
    for item in div.dl.find_all('dd'):
        dds.append(''.join(item.stripped_strings))
    res = []
    for dt, dd in zip(dts, dds):
        res.append((dt, dd))
    return date, res


def scrape_detail(rf):
    soup = BeautifulSoup(rf, 'lxml')
    # date_string = soup.find(id='firstHeading').string
    all_items = []
    all_h3 = soup.find(class_='mw-parser-output').find_all('h3')
    for h3 in all_h3:
        uls = h3.find_next_sibling('ul')
        for li in uls.find_all('li'):
            all_items.append(''.join(li.stripped_strings))
    return all_items


def calculate_datetime(date_string):
    date_nums = re.findall('\d+', date_string)
    if len(date_nums) == 2:
        date = datetime(datetime.now().year, *[int(x) for x in date_nums])
    elif len(date_nums) == 3:
        date = datetime(*[int(x) for x in date_nums])
    else:
        date = datetime.now()
    passed_day = (date - datetime(datetime.now().year, 1, 1)).days + 1
    remain_day = (datetime(datetime.now().year + 1, 1, 1) - date).days - 1
    return passed_day, remain_day


def get_single_day(date_string):
    yy, mm, day = date_string.split('-')
    content = download_page(SINGLE_DAY_URI.format(month=mm, day=day))
    return scrape_detail(content)


pool = ConnectionPool(host='localhost', port=6379, db=1)
redis_proxy = Redis(connection_pool=pool)


def get_data_from_redis(date_string):  # format为 2017-11-16
    if redis_proxy.exists(date_string):
        res = redis_proxy.get(date_string).decode('utf-8').split('||')
    else:
        res = get_single_day(date_string)
        redis_proxy.set(date_string, '||'.join(res))
    redis_proxy.expire(date_string, timedelta(days=3))  # 刷新缓存时间

    return sample(res, 1)


if __name__ == '__main__':
    pass

