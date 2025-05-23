import configparser
import csv
from datetime import datetime, timedelta

import Services
import Hash_Table
from Services import DataServices



def open_store_packages(data_service:DataServices):
    package_info_table = Hash_Table.Hash_Table()
    #load in the package file data
    package_data = data_service.get_data_file('package_file')

    # make packages and store in hash table
    return make_packages(data_service,package_data,package_info_table)

def make_packages(data_service,data_lines,package_info_table:Hash_Table):
        # load in the package components
        for data_line in data_lines:
            # assign the unique id to the new package
            temp_id = data_line[0]
            if temp_id.isdigit():
                temp_id = int(temp_id)
            try:
                new_package = Package(temp_id)
                new_package.street_address = data_line[1]
                new_package.city = data_line[2]
                new_package.state = data_line[3]
                new_package.zip_code = data_line[4]

                deadline_date = ''
                deadline_time=data_line[5].strip()
                if deadline_time =='EOD':
                    deadline_time='6:00 PM'

                new_package.delivery_deadline =  Services.convert_str_datetime(deadline_date,deadline_time)
                new_package.weight_kg = data_line[6]
                new_package.special_notes = data_line[7]
                package_delay = data_line[8]
                if package_delay != '':
                    try:
                        file_delay_time = Services.convert_str_datetime('',package_delay)
                    except ValueError:
                        file_delay_time = None
                else:
                    file_delay_time=None
                new_package.delayed_delivery_time = file_delay_time
                delivery_truck = data_line[9]
                if delivery_truck.isdigit():
                    new_package.delivery_truck = int(data_line[9])
                new_package.co_delivery = data_line[10]
                new_package.new_address_needed = data_line[11]

                # add pacakge to package info table
                package_info_table.add(new_package.id, new_package)


            except ValueError as e:
                print(f'{e.args[0]} A new package was not created.')

        return package_info_table

#lookup function (by package id) to return package components
def get_package(package_info_table:Hash_Table,package_id:int):
    found_package=package_info_table.get(package_id)
    if found_package is None:
        return None
    else:
        return found_package



def package_status_all(package_info_table:Hash_Table, package_id=0, time:datetime=timedelta(0)):
    Services.print_line()
    package_list=None

    #get all packages
    if package_id==0:
        print(f'{'UTPPS Package Delivery Summary - All Packages':^220}')
        package_list=package_info_table.get_all()
    #get a specific package
    else:
        summary_title = f'UTPPS Package Delivery Summary for Package ID {package_id}'
        print(f'{summary_title:^220}')
        package_list = [package_info_table.get(package_id)]

    for package in package_list:
        Services.print_line()
        print(package.print_status(time))
        Services.print_line()



class Package:
    __package_ids=set()

    def __init__(self, package_id:'int'):
        # check for duplicate unique integer id
        if package_id in Package.__package_ids:
            raise ValueError(f'Package with ID {package_id} already exists.', package_id)
        elif not type(package_id) is int:
            raise ValueError(f'Package with ID {package_id} is not an integer.', package_id)

        self.id = package_id
        self.__package_ids.add(package_id)
        self.street_address = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.delivery_deadline = ''
        self.weight_kg = ''
        self.special_notes = ''
        self.delayed_delivery_time = None
        self.delivery_truck = ''
        self.co_delivery = ''
        self.new_address_needed = ''
        self.delivery_status=''
        self.delivery_end_datetime=None
        self.delivery_start_datetime = None
        self.delivery_deadline=None

    def get_address(self):
        address_zip=f'{self.street_address}|{self.zip_code}'
        return address_zip

    def print_status(self, time:datetime):
        #use the time to retrieve the correct package status information

        #check for address change based on time
        if self.new_address_needed != 'No':
            try:
                new_address_needed_time = datetime.strptime(self.new_address_needed, '%I:%M %p')
                if new_address_needed_time > time:
                    address_at_time = '410 S State St'
                    zip_at_time = '84111'
                else:
                    address_at_time = self.street_address
                    zip_at_time = self.zip_code
            except ValueError:
                new_address_needed_time=None
                address_at_time = self.street_address
                zip_at_time = self.zip_code
        else:
            address_at_time = self.street_address
            zip_at_time = self.zip_code

        #get delivery info based on time
        if self.delivery_end_datetime < time:
            status_at_time='delivered'
            delivery_endtime_at_time = self.delivery_end_datetime
            truck_at_time = f'Truck #:{self.delivery_truck}'
        elif self.delivery_end_datetime > time > self.delivery_start_datetime:
            status_at_time='En route'
            delivery_endtime_at_time = ''
            truck_at_time = f'Truck #:{self.delivery_truck}'
        elif self.delayed_delivery_time is not None and self.delayed_delivery_time > time:
            status_at_time=f'Delayed - expected to arrive at hub {self.delayed_delivery_time}'
            delivery_endtime_at_time = ''
            truck_at_time = ''
        else:
            status_at_time='at hub'
            delivery_endtime_at_time = ''
            truck_at_time = ''


        return f'Package: {self.id} Weight: {self.weight_kg}kg Delivery Address: {address_at_time} {self.city}, {self.state} {zip_at_time}\nDelivery Status at {time}: {status_at_time} {delivery_endtime_at_time} {truck_at_time}'
    def __str__(self):
        return f'Package: {self.id} Weight: {self.weight_kg}kg Delivery Address: {self.street_address} {self.city}, {self.state} {self.zip_code}\nTruck #:{self.delivery_truck} Delivery Status: {self.delivery_status} {self.delivery_end_datetime}'