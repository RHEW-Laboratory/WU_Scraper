import bs4
import csv
import re
import requests


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


def _url_builder(airport, start_date, end_date):
    """Accepts three mandatory parameters airport, start_date, and end_date.
    These are used to construct a Weather Underground Specific URL, as well
    as set the filename for the csv that is produced by this script.
    """
    airport = airport.upper()
    s_year, s_month, s_day = start_date.split('-')
    e_year, e_month, e_day = end_date.split('-')

    base_url = 'https://www.wunderground.com/history/airport/'
    url = base_url + "{}/{}/{}/{}".format(
        airport, s_year, int(s_month), int(s_day)
    )
    url += '/CustomHistory.html?dayend={}&monthend={}&yearend={}'.format(
        int(e_day), int(e_month), e_year
    )
    url += '&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='
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


def write_headers(fieldnames):
    with open(OUTPUT_FILENAME, 'w') as csv_file:
        headerWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        headerWriter.writeheader()


def _row_writer(row, fieldnames):
    with open(OUTPUT_FILENAME, 'a') as csv_file:
        rowWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)

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


def _extract_table(soup_obj):
    """Parses Soup object to find each row within the 'Weather History
    & Observations` HTML table of a particular Weather Underground Custom
    History page.
    """
    year = int
    month = str
    day = int

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
                    _row_writer(row, FIELDNAMES)


def main():
    url = _url_builder(airport, start_date, end_date)
    soup_obj = _scrape_the_underground(url)
    write_headers(FIELDNAMES)
    _extract_table(soup_obj)


if __name__ == "__main__":
    # airport = input("Enter Airport Code: (ex. SFO): ")
    # start_date = input("Enter a start date (YYYY-MM-DD): ")
    # end_date = input("Enter a start date (YYYY-MM-DD): ")
    
    airport = "KLIT"
    start_date = '1948-01-01'
    end_date = '2017-02-01'
    OUTPUT_FILENAME = "{}_{}_{}.csv".format(
        airport.upper(), start_date, end_date
    )
    main()
