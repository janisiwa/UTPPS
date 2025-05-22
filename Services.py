import os
import configparser
import csv
from tracemalloc import take_snapshot


from datetime import datetime,date,timedelta


def read_config():
    # get package data file location from application config file
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.getcwd(), 'app_config.ini')
    config.read(config_file_path)
    return config

def print_line():
    #decorative line for spacing in the UI
    print('-'*220)

def print_new_section():
    print('\n\n')

class DataServices:

    def get_config_info(self, section: str, info_type: str):
        config = read_config()
        return config.get(section, info_type)

    def get_data_file(self, file_type:str):
        config = read_config()
        package_file_location = config.get('data_sources', file_type)

        # open the file
        data = open(package_file_location, encoding='utf-8-sig')
        csv_reader = csv.reader(data)
        data_lines = list(csv_reader)
        return data_lines



    def convert_str_datetime(self,str_date:str='',str_time:str=''):
        #if date not provided, use today's date
        if str_date=='':
            today = date.today()
            str_date= f'{today.month}-{today.day}-{today.strftime('%Y')}'

        #if time not provided, use 12 am
        if str_time == '':
            str_time= '12:00 AM'

        str_datetime = f'{str_date} {str_time}'
        return datetime.strptime(str_datetime, '%m-%d-%Y %I:%M %p')

    def next_stop_time(self,start_time:datetime,distance:float):
        #retrieve the speed in miles per hour
        speed = float(DataServices.get_config_info(self,'truck_info','speed_mph').strip())

        #distance/speed = how many hours it takes
        travel_hours = distance/speed

        #how many minutes it takes
        travel_minutes = travel_hours*60

        return start_time + timedelta(minutes=travel_minutes)
