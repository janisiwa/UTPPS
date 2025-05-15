import configparser

import Hash_Table
import os
import configparser


class Package:

    def __init__(self, package_id: int, package_info_table:'Hash_Table'):
        #assign the unique id to the new package
        self.id= package_id

        #check for duplicate unique id
        if package_info_table.get(package_id):
            raise ValueError(f"Package with id {package_id} already exists")

        #get package data file location from application config file
        config = configparser.ConfigParser()
        config_file_path = os.path.join(os.getcwd(), 'app_config.ini')
        config.read(config_file_path)
        package_file_location = config.get('data_sources','package_file')


        #load in the package components
        self.street_address='195 W Oakland Ave'
        self.city='Salt Lake City'
        self.state='UT'
        self.zip_code='84115'
        self.delivery_deadline_time='10:30:00'
        self.delivery_deadline_date='05/15/2025'
        self.weight_kg='21'
        self.special_notes='can only be on truck 2'
        self.delayed_delivery_time='10:30:00'
        self.delivery_truck='Truck 2'
        self.co_delivery='15,19'
        self.new_address_needed='Yes'

        #add pacakge to package info table
        package_info_table.add(self.id, self)