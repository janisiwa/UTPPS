import configparser
import csv
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

                new_package.delivery_deadline =  data_service.convert_str_datetime(deadline_date,deadline_time)
                new_package.weight_kg = data_line[6]
                new_package.special_notes = data_line[7]
                new_package.delayed_delivery_time = data_line[8]
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

class Package:
    __package_ids=set()

    def __init__(self, package_id:'int'):
        # check for duplicate unique integer id
        if package_id in Package.__package_ids:
            raise ValueError(f'Package with ID {package_id} already exists.', package_id)
        elif not type(package_id) is int:
            raise ValueError(f'Package with ID {package_id} is not an integer.', package_id)

        self.id = package_id
        
        self.street_address = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.delivery_deadline = ''
        self.weight_kg = ''
        self.special_notes = ''
        self.delayed_delivery_time = ''
        self.delivery_truck = ''
        self.co_delivery = ''
        self.new_address_needed = ''
        self.delivery_status=''
        self.delivery_time=''
        self.delivery_date=''



    def __str__(self):
        return f'Package: {self.id} {self.weight_kg}\nDelivery Details: {self.street_address} {self.city}, {self.state}  {self.zip_code}   {self.delivery_deadline_time} {self.delivery_truck} \nSpecial Notes:  {self.special_notes} {self.delayed_delivery_time} {self.co_delivery}  {self.new_address_needed}'