import requests
import datetime
import csv
import gymstalker.models


def obtain_data() -> int:
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


def save_data() -> str:
    # dt_now stores current time
    dt_now = datetime.datetime.now()

    # convert datetime to string
    dt_now_str = dt_now.strftime("%m/%d/%Y, %H:%M:%S")

    # obtain current gym occupation
    currentvisitors = obtain_data()
    if not isinstance(currentvisitors, int):
        return f'{dt_now_str}: An error occurred while querying the data'

    # append datetime string and gym occupation to csvfile
    # with open('data.csv', 'a', newline='') as csvfile:
    #     datawriter = csv.writer(csvfile, delimiter=',')
    #     datawriter.writerow([dt_now_str] + [currentvisitors])

    # return current date and time and the number of visitors
    data = gymstalker.models.data_entry.objects.create(
        date=dt_now,
        visitors=currentvisitors
    )
    data.save()
    return f'{dt_now_str}: {currentvisitors} Visitors'



