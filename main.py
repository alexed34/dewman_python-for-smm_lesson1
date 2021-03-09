import datetime
import os
import time

import plotly.graph_objs as go
import requests
from dotenv import load_dotenv

load_dotenv()


def get_text(ACCESS_TOKEN, start_time, end_time):
    url = f'https://api.vk.com/method/newsfeed.search?q={text_request}&' \
          f'start_time={start_time}&end_time={end_time}&' \
          f'access_token={ACCESS_TOKEN}&v=5.130'
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_last_dates(num):
    dates = []
    for i in range(1, num + 1):
        today = datetime.date.today()
        day_before = today - datetime.timedelta(days=i)
        timestamp_yesterday = datetime.datetime(year=day_before.year,
                                                month=day_before.month,
                                                day=day_before.day).timestamp()
        date = (
            datetime.date(day_before.year, day_before.month, day_before.day),
            timestamp_yesterday, timestamp_yesterday + 86400)

        dates.append(date)
    return dates


def get_total_count(response):
    total_count = response['response']['total_count']
    return total_count


def get_count_stat(dates):
    count_stat = []
    for i in dates:
        response = get_text(ACCESS_TOKEN, i[1], i[2])
        total_count = get_total_count(response)
        count_stat.append(total_count)
        print(i[0])
        time.sleep(1)
    return count_stat


def show_bar(dates, count_stat):
    dates = [i[0] for i in dates]
    fig = go.Figure([go.Bar(x=dates, y=count_stat)])
    fig.show()


def main():
    dates = get_last_dates(7)
    count_stat = get_count_stat(dates)
    show_bar(dates, count_stat)


if __name__ == '__main__':
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    text_request = 'Coca-Cola'
    main()
