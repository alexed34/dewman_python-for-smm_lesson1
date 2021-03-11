import datetime
import os
import time
import logging

import plotly.graph_objs as go
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(message)s')



def get_text(access_token, start_time, end_time, text_request):
    params = {'q': text_request,
              'access_token': access_token,
              'start_time': start_time,
              'end_time': end_time,
              'v': '5.130'
              }
    url = f'https://api.vk.com/method/newsfeed.search'
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_last_dates(num):
    dates = []
    for day in range(1, num + 1):
        today = datetime.date.today()
        day_before = today - datetime.timedelta(days=day)
        timestamp_yesterday = datetime.datetime(year=day_before.year,
                                                month=day_before.month,
                                                day=day_before.day).timestamp()
        seconds_in_day = 86400
        date = (
            datetime.date(day_before.year, day_before.month, day_before.day),
            timestamp_yesterday, timestamp_yesterday + seconds_in_day)

        dates.append(date)
    return dates


def get_count_stat(dates, access_token, text_request):
    count_stat = []
    for data, start_time, end_time in dates:
        response = get_text(access_token, start_time, end_time, text_request)
        total_count = response['response']['total_count']
        count_stat.append(total_count)
        logging.info(data)
        time.sleep(1)
    return count_stat


def show_bar(dates, count_stat):
    dates = [data[0] for data in dates]
    fig = go.Figure([go.Bar(x=dates, y=count_stat)])
    fig.show()


def main():
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    text_request = 'Coca-Cola'
    dates = get_last_dates(7)
    count_stat = get_count_stat(dates, access_token, text_request)
    show_bar(dates, count_stat)


if __name__ == '__main__':
    main()
