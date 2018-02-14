#!/usr/bin/python
"""
Title: Weather Underground Grabber
author: Lawerence Lee

Description: This program scrapes airport weather data stored on Weather
Underground's website. The data will output into a csv file and be named
with the aiport code and dates provided.

Parameters
----------
AIRPORT : str
    The code that designates a particular airport (ex. SFO is the airport
    code for San Francisco International).
START_DATE : str
    The date you'd like to start scraping data from.
END_DATE : str
    The final date you'd like to scrape data from.

Generates
---------
A csv containing the weather data you requested.


Copyright (c) 2018 LawerenceLee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import bs4
import csv
import datetime
import os
import re
import requests


AIRPORT = str
START_DATE = str
END_DATE = str
OUTPUT_FILENAME = ''
URL = ''


FIELDNAMES = [
    'date',
    'high_temp_ºF', 'ave_temp_ºF', 'low_temp_ºF',
    'high_dew_pt_ºF', 'ave_dew_pt_ºF', 'low_dew_pt_ºF',
    'high_humidity_%', 'ave_humidity_%', 'low_humidity_%',
    'high_sea_lvl_press_in', 'ave_sea_lvl_press_in', 'low_sea_lvl_press_in',
    'high_visibitlity_mi', 'ave_visibitlity_mi', 'low_visibitlity_mi',
    'high_wind_mph', 'ave_wind_mph', 'low_wind_mph',
    'total_precip_in',
    'events'
]

MONTH_DICT = {
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
}


def clear():
    """Clears the command prompt"""
    os.system('cls' if os.name == 'nt' else 'clear')


def _url_builder(AIRPORT, START_DATE, END_DATE):
    """Accepts three mandatory parameters AIRPORT, START_DATE, and END_DATE.
    These are used to construct a Weather Underground Specific URL, as well
    as set the filename for the csv that is produced by this script.
    """
    AIRPORT = AIRPORT.upper()
    s_year, s_month, s_day = START_DATE.split('-')
    e_year, e_month, e_day = END_DATE.split('-')

    base_url = 'https://www.wunderground.com/history/airport/'
    url = base_url + "{}/{}/{}/{}".format(
        AIRPORT, s_year, int(s_month), int(s_day)
    )
    url += '/CustomHistory.html?dayend={}&monthend={}&yearend={}'.format(
        int(e_day), int(e_month), e_year
    )
    url += '&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='
    # print(url)
    return url


def _scrape_the_underground(url):
    """Scrapes the web page specified by url and passes the resulting HTML
    to a Beautiful Soup Object.
    """
    res = requests.get(url)
    res.raise_for_status()
    soup_obj = bs4.BeautifulSoup(res.text, "html.parser")
    return soup_obj


def _check_day_str(day):
    """If day has a length of one a zero is added before it, otherwise day is
    simply returned.
    """
    if len(day) == 1:
        day = '0{}'.format(day)
    return day


def _build_row(td_tags, date):
    """Takes a list of HTML <td> tags as strings, extracts each of their values and
    adds them to a list. Escape characters are removed from the final index.
    The first value is replaced by the date.
    """
    row_vals = [x.getText().strip() for x in td_tags]
    row_vals[-1] = re.sub('\n', '', row_vals[-1])
    row_vals[-1] = re.sub('\t', '', row_vals[-1])
    row_vals[0] = date
    return row_vals


def _write_headers():
    """Writes the column headers to the csv."""
    with open(OUTPUT_FILENAME, 'w') as csv_file:
        headerWriter = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        headerWriter.writeheader()


def _row_writer(row):
    """Writes each row of data to the csv."""
    with open(OUTPUT_FILENAME, 'a') as csv_file:
        rowWriter = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)

        rowWriter.writerow({
            'date': row[0],
            'high_temp_ºF': row[1],
            'ave_temp_ºF': row[2],
            'low_temp_ºF': row[3],
            'high_dew_pt_ºF': row[4],
            'ave_dew_pt_ºF': row[5],
            'low_dew_pt_ºF': row[6],
            'high_humidity_%': row[7],
            'ave_humidity_%': row[8],
            'low_humidity_%': row[9],
            'high_sea_lvl_press_in': row[10],
            'ave_sea_lvl_press_in': row[11],
            'low_sea_lvl_press_in': row[12],
            'high_visibitlity_mi': row[13],
            'ave_visibitlity_mi': row[14],
            'low_visibitlity_mi': row[15],
            'high_wind_mph': row[16],
            'ave_wind_mph': row[17],
            'low_wind_mph': row[18],
            'total_precip_in': row[19],
            'events': row[20],
        })
        print(row)


def _extract_table(soup_obj, row):
    """Parses Soup object to find each row of data within the 'Weather History
    & Observations` HTML table of a particular airport's Weather Underground
    Custom History page.
    """
    year = int
    month = str
    day = int

    table = soup_obj.find(id='obsTable')
    # print(table)
    # print(len(table.contents))
    # input()
    while table is None or len(table.contents) == 1:
        blank_row = [
            row[0], '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
            '-', '-', '-', '-', '-', '-', '-', '-', '-', '',
        ]
        _row_writer(blank_row)
        row[0] = _add_one_day(row[0])
        START_DATE = _add_one_day(row[0])
        URL = _url_builder(AIRPORT, START_DATE, END_DATE)
        soup_obj = _scrape_the_underground(URL)
        table = soup_obj.find(id='obsTable')

    for tag in table.contents:
        if type(tag) == bs4.element.Tag:
            if tag.find('th'):
                year = tag.find('th').getText()
            elif tag.find('td'):
                td_tags = tag.find_all('td')
                first_tag = td_tags[0].getText()
                if len(first_tag) == 3:
                    month = first_tag.lower()
                else:
                    day = _check_day_str(first_tag)
                    date = '{}-{}-{}'.format(year, MONTH_DICT[month], day)
                    row = _build_row(td_tags, date)
                    _row_writer(row)
    return row[0], row


def _check_date_match(last_date, END_DATE):
    """Checks if the last date added to the csv matches the value entered for
    'END_DATE'.
    """
    if last_date == END_DATE:
        return True, last_date
    else:
        new_start = _add_one_day(last_date)
        return False, new_start


def _add_one_day(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    new_date = date + datetime.timedelta(days=1)
    new_date = new_date.strftime('%Y-%m-%d')
    return new_date


def _start_message():
    """Writes and says a starting download message."""
    clear()
    print('Starting Download')
    try:
        os.system("say 'Starting download'")
    except Exception as e:
        print(e, '\n')
        print("SCRIPT IS NOT BROKEN, DON'T WORRY")


def _end_message():
    """Writes and says a finished download message."""
    clear()
    print("Finished Download")
    try:
        os.system("say 'Download Complete'")
    except Exception:
        pass


def main(AIRPORT, START_DATE, END_DATE):
    row = [START_DATE]
    _write_headers()
    _start_message()
    date_match = False
    while date_match is False:
        URL = _url_builder(AIRPORT, START_DATE, END_DATE)
        soup_obj = _scrape_the_underground(URL)
        last_date, row = _extract_table(soup_obj, row)
        date_match, START_DATE = _check_date_match(
            last_date, END_DATE
        )
    _end_message()


if __name__ == "__main__":
    AIRPORT = input("Enter Airport Code: (ex. SFO): ")
    START_DATE = input("Enter a start date (YYYY-MM-DD): ")
    END_DATE = input("Enter an end date (YYYY-MM-DD): ")
    # AIRPORT = 'KOAK'
    # START_DATE = '1943-01-01'
    # END_DATE = '2017-02-12'
    OUTPUT_FILENAME = "{}_{}_{}.csv".format(
        AIRPORT.upper(), START_DATE, END_DATE
    )
    clear()
    main(AIRPORT, START_DATE, END_DATE)
