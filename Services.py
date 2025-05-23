import os
import configparser
import csv
from tracemalloc import take_snapshot
from datetime import datetime, date, timedelta


def convert_str_datetime(str_date: str = '', str_time: str = ''):
    """Convert date and time strings into a datetime object.

    If no date string is provided, the current date is used.
    If no time string is provided, 12:00 AM is used.

    Args:
        str_date (str, optional): Date string in 'MM-DD-YYYY' format. Defaults to ''.
        str_time (str, optional): Time string in 'HH:MM AM/PM' format. Defaults to ''.

    Returns:
        datetime: A datetime object representing the combined date and time.
    """
    if str_date == '':
        today = date.today()
        str_date = f'{today.month}-{today.day}-{today.strftime("%Y")}'

    if str_time == '':
        str_time = '12:00 AM'

    str_datetime = f'{str_date} {str_time}'
    return datetime.strptime(str_datetime, '%m-%d-%Y %I:%M %p')


def read_config():
    """Read the application configuration file.

    The config file is expected to be named 'app_config.ini' and located in the current working directory.

    Returns:
        configparser.ConfigParser: The loaded configuration parser object.
    """
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.getcwd(), 'app_config.ini')
    config.read(config_file_path)
    return config


def print_line():
    """Print a decorative horizontal line for UI spacing."""
    print('-' * 220)


def print_new_section():
    """Print two newlines to create a section break in UI output."""
    print('\n\n')


def get_config_info(section: str, info_type: str):
    """Retrieve specific configuration information from the config file.

    Args:
        section (str): The section name in the config file.
        info_type (str): The specific configuration key within the section.

    Returns:
        str: The configuration value corresponding to the given section and key.
    """
    config = read_config()
    return config.get(section, info_type)


def get_data_file(file_type: str):
    """Load data from a CSV file specified in the config under 'data_sources'.

    Args:
        file_type (str): The key identifying the file path in the config 'data_sources' section.

    Returns:
        list[list[str]]: A list of rows read from the CSV file, each row as a list of strings.
    """
    config = read_config()
    package_file_location = config.get('data_sources', file_type)

    # open the file
    data = open(package_file_location, encoding='utf-8-sig')
    csv_reader = csv.reader(data)
    data_lines = list(csv_reader)
    return data_lines


def next_stop_time(start_time: datetime, distance: float):
    """Calculate the arrival time at the next stop based on start time and travel distance.

    Uses the truck speed (mph) defined in the config under 'truck_info'.

    Args:
        start_time (datetime): The departure time from the current location.
        distance (float): The distance to the next stop in miles.

    Returns:
        datetime: The estimated arrival time at the next stop.
    """
    # retrieve the speed in miles per hour
    speed = float(get_config_info('truck_info', 'speed_mph').strip())

    # distance/speed = how many hours it takes
    travel_hours = distance / speed

    # how many minutes it takes
    travel_minutes = travel_hours * 60

    return start_time + timedelta(minutes=travel_minutes)
