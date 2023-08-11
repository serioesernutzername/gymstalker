import codecs
import os
from selenium import webdriver
import csv
import datetime
import re


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
    driver = webdriver.Firefox()

    # Define the URL
    url = "https://www.mysports.com/studio/c3BvcnRmYWJyaWs6MTIxMDAwOTc0MA%3D%3D"

    # load the web page
    driver.get(url)

    # set maximum time to load the web page in seconds
    driver.implicitly_wait(10)

    n = os.path.join("C:/Users/morit/Downloads/", "Page.html")
    # open file in write mode with encoding
    f = codecs.open(n, "w", "utf−8")
    # obtain page source
    h = driver.page_source
    # write page source content to file
    f.write(h)
    # close browser
    driver.quit()


obtain_data()
save_data()
