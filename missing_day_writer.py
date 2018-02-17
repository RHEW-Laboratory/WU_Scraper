"""A python script that checks for missing rows of data in a csv by changes of
more than one day in the date column
"""

import csv
import datetime
import os


FILEPATH = str
BLANK_ROW = ['' for _ in range(21)]


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


def clear():
    """Clears the command prompt"""
    os.system('cls' if os.name == 'nt' else 'clear')


def _add_one_day(date):
    """Increases the date by one day using the datetime library"""
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date + datetime.timedelta(days=1)
    date = date.strftime('%Y-%m-%d')
    return date


def insert_blank_records(row, current_date):
    record_date = row['date']
    while current_date != record_date:
        BLANK_ROW[0] = current_date
        row_writer(BLANK_ROW)
        current_date = _add_one_day(current_date)
    build_row(row)
    return _add_one_day(row['date'])


def build_row(row_dict):
    row = []
    keys = row_dict.keys()
    for key in keys:
        row.append(row_dict[key])
    row_writer(row)


def write_headers():
    """Writes the column headers to the csv."""
    with open(FILEPATH, 'w') as csv_file:
        headerWriter = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        headerWriter.writeheader()


def row_writer(row):
    """Writes each row of data to the csv."""
    with open(FILEPATH, 'a') as csv_file:
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
            'events': '{}'.format(row[20]),
        })
        print(row)


def main():
    filename = FILEPATH.split('/')[-1]
    name, file_type = filename.split('.')
    airport, start_date, end_date = name.split("_")
    backup = name + '.backup'
    os.replace(FILEPATH, backup)
    write_headers()
    with open(backup) as csv_file:
        reader = csv.DictReader(csv_file)
        current_date = start_date
        for row in reader:
            if row['date'] == current_date:
                build_row(row)
                current_date = _add_one_day(row['date'])
            elif row['date'] != current_date:
                current_date = insert_blank_records(row, current_date)
    os.remove(backup)


if __name__ == "__main__":
    clear()
    FILEPATH = input("Enter CSV filepath: ")
    main()
