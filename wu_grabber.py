import bs4
import re
import requests


FIELDNAMES = [
    'date'
    'high_temp_ºF', 'ave_temp_ºF', 'low_temp_ºF',
    'high_dew_pt_ºF', 'ave_dew_pt_ºF', 'low_dew_pt_ºF',
    'high_humidity_%', 'ave_humidity_%', 'low_humidity_%',
    'high_sea_lvl_press_in', 'ave_sea_lvl_press_in', 'low_sea_lvl_press_in',
    'high_visibitlity_mi', 'ave_visibitlity_mi', 'low_visibitlity_mi',
    'high_wind_mph', 'ave_wind_mph', 'low_wind_mph',
    'high_precip_in', 'ave_precip_in', 'low_precip_in',
    'events'
]

MONTH_DICT = {
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
}


def _url_builder(airport, start_date, end_date):
    url = 'https://www.wunderground.com/history/airport/KLIT/1948/2/12/CustomHistory.html?dayend=12&monthend=2&yearend=2018&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo='
    return url
    

def _scrape_the_underground(url):
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


# def _row_writer(row):
#     with open()


def _extract_table(soup_obj):
    year = int
    month = str
    day = int

    table = soup_obj.find(id='obsTable')
    for tag in table.contents:
        if type(tag) == bs4.element.Tag:
            if tag.find('th'):
                # print('\nTH TAG')
                year = tag.find('th').getText()
            elif tag.find('td'):
                # print('\nTD TAG')
                td_tags = tag.find_all('td')
                first_tag = td_tags[0].getText()
                if len(first_tag) == 3:
                    month = first_tag.lower()
                else:
                    day = _check_day_str(first_tag)
                    date = '{}-{}-{}'.format(year, MONTH_DICT[month], day)
                    row = _build_row(td_tags, date)
                    print(row)


def main():
    # _url_builder(airport, start_date, end_date)
    url = _url_builder('SFO', '1990-12-05', '1997-12-05')
    soup_obj = _scrape_the_underground(url)
    _extract_table(soup_obj)


if __name__ == "__main__":
    # airport = input("Enter Airport Code: (ex. SFO): ").upper()
    # start_date = input("Enter a start date (YYYY-MM-DD): ")
    # end_date = input("Enter a start date (YYYY-MM-DD): ")
    main()
