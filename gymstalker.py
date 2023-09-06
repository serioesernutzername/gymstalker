import csv
import datetime
import re
import requests


def save_data():
    # dt_now stores current time
    dt_now = datetime.datetime.now()
    print("Current time: ", dt_now)

    # convert datetime to string
    dt_now_str = dt_now.strftime("%m/%d/%Y, %H:%M:%S")

    # create regex for gym occupation
    regex = r'[0-9]+[&][n][b][s][p][;][B][e][s][u][c][h][e][r]'

    # search Page.html with regex and get result
    with open('Page.html', 'r') as infile:
        html_page = infile.read()
        results = re.findall(regex, html_page)
        result = str(results[0])
        gym_occupation = re.search('[0-9]*', result).group()

    # append date time string and gym occupation to csvfile
    with open('data.csv', 'a', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',')
        datawriter.writerow([dt_now_str] + [gym_occupation])


def obtain_data():
    url = "https://www.mysports.com/nox/public/v1/studios/1210009740/utilization/v2/active-checkin"
    headers = {
        "x-tenant": "sportfabrik",
        "DNT": "1",
    }

    result = requests.get(url, headers=headers)
    return result
