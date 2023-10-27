import csv
import datetime
import os
import requests
import schedule
import time


def data_retrieve(url: str) -> requests.models.Response:
    """ Send an HTTP GET request to a "mysports.com" API-URL and return the response. """

    # headers to send with the request
    headers = {
        "Content-Type": "application/json",
        "x-tenant": "sportfabrik",
        "DNT": "1",
    }

    # send GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # return the response
    return response


def data_retrieve_open() -> bool:
    """ Check whether the gym is open. """

    # URL to obtain data from
    url = "https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/today"

    # get HTTP response
    response = data_retrieve(url)

    # convert response to JSON format and return the first value of the "current" key
    for x in range(len(response.json())):
        if response.json()[x - 1]['current'] is True:
            return True
    return False


def data_retrieve_count() -> int:
    """ Retrieve the current visitor count. """

    # URL to obtain data from
    url = "https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/active-checkin"

    # get HTTP response
    response = data_retrieve(url)

    # convert response to JSON format and return the value of the "value" key
    return response.json()['value']


def data_retrieve_percentage() -> int:
    """ Retrieve the current capacity utilization in percent. """

    # URL to obtain data from
    url = "https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/today"

    # get HTTP response
    response = data_retrieve(url)

    # convert response to JSON format and return the value of the "percentage" key
    for x in range(len(response.json())):
        if response.json()[x - 1]['current'] is True:
            return response.json()[x - 1]['percentage']
    return 0


def data_save() -> str:
    """ Save the current visitor information to a csv file. """

    # dt_now stores current time
    dt_now = datetime.datetime.now()

    # convert datetime to string
    dt_now_str = dt_now.strftime("%m/%d/%Y, %H:%M:%S")

    # if the gym is open, retrieve visitor data
    if data_retrieve_open():
        # retrieve current gym occupation
        visitors = data_retrieve_count()
        visitors_percent = data_retrieve_percentage()

        # if the retrieved data does not fulfill our requirements, return error message
        if not isinstance(visitors, int) or not isinstance(visitors_percent, int):
            return f'{dt_now_str}: An error occurred while querying the data'
        elif visitors < 0 or not 0 <= visitors_percent <= 100:
            return f'{dt_now_str}: The retrieved values are strange: {visitors} Visitors ({visitors_percent}%)'

        # append datetime string and gym occupation to csvfile
        with open('data.csv', 'a', newline='') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',')
            datawriter.writerow([dt_now_str] + [visitors] + [visitors_percent])

        # return current date and time, the number of visitors and percentage
        return f'{dt_now_str}: {visitors} Visitors ({visitors_percent}%)'

    # if the gym is closed, return error message
    else:
        return f'{dt_now_str}: No data available'


def job():
    """ Job to be executed in the specified time intervals. """

    # call data_save() and print feedback to the console
    print(data_save())


def main():
    # create a new "data.csv", if the file does not exist
    if not os.path.exists('data.csv'):
        with open('data.csv', 'w', newline='') as csvfile:
            csvfile.write('Time,Visitors,Percentage\n')

    # every 15 minutes job() is called through task scheduling
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":15").do(job)
    schedule.every().hour.at(":30").do(job)
    schedule.every().hour.at(":45").do(job)

    # print feedback to the console
    print('Beginning to collect visitor information from'
        + 'https://www.mysports.com/studio/c3BvcnRmYWJyaWs6MTIxMDAwOTc0MA%3D%3D ...')

    # loop so that the scheduling tasks keep on running all time
    while True:
        # checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
