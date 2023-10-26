import requests
import datetime
import csv
import schedule
import time


def check_if_open() -> bool:
    # URL to obtain current state from
    url = "https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/today"

    # headers to send with the request
    headers = {
        "Content-Type": "application/json",
        "x-tenant": "sportfabrik",
        "DNT": "1",
    }

    # send GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # convert response to JSON format and return the first value of the "current" key
    for x in range(len(response.json())):
        if response.json()[x - 1]['current'] is True:
            return True
    return False


def obtain_data_count() -> int:
    # URL to obtain data from
    url = "https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/active-checkin"

    # headers to send with the request
    headers = {
        "Content-Type": "application/json",
        "x-tenant": "sportfabrik",
        "DNT": "1",
    }

    # send GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # convert response to JSON format and return the value of the "value" key
    return response.json()['value']


def obtain_data_percentage() -> int:
    # URL to obtain data from
    url = "	https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/today"

    # headers to send with the request
    headers = {
        "Content-Type": "application/json",
        "x-tenant": "sportfabrik",
        "DNT": "1",
    }

    # send GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # convert response to JSON format and return the value of the "percentage" key
    for x in range(len(response.json())):
        if response.json()[x - 1]['current'] is True:
            return response.json()[x - 1]['percentage']
    return 0


def save_data() -> str:
    # dt_now stores current time
    dt_now = datetime.datetime.now()

    # convert datetime to string
    dt_now_str = dt_now.strftime("%m/%d/%Y, %H:%M:%S")

    if check_if_open():
        # obtain current gym occupation and percentage
        visitors = obtain_data_count()
        if not isinstance(visitors, int):
            return f'{dt_now_str}: An error occurred while querying the data'
        visitors_percent = obtain_data_percentage()
        if not isinstance(visitors_percent, int):
            return f'{dt_now_str}: An error occurred while querying the data'

        # append datetime string, gym occupation and percentage to csvfile
        with open('data.csv', 'a', newline='') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',')
            datawriter.writerow([dt_now_str] + [visitors] + [visitors_percent])

        # return current date and time, the number of visitors and percentage
        return f'{dt_now_str}: {visitors} Visitors ({visitors_percent}%)'

    else:
        return f'{dt_now_str}: No data available'


def job():
    print(save_data())


def main():
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":15").do(job)
    schedule.every().hour.at(":30").do(job)
    schedule.every().hour.at(":45").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
