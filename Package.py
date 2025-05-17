import configparser
import csv

import Hash_Table


class Package:
    __package_ids=set()

    def __init__(self, package_id:'int'):
        # check for duplicate unique id
        if package_id in Package.__package_ids:
            raise ValueError(f"Package with ID {package_id} already exists.", package_id)

        self.id = package_id
        
        self.street_address = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.delivery_deadline_time = ''
        self.weight_kg = ''
        self.special_notes = ''
        self.delayed_delivery_time = ''
        self.delivery_truck = ''
        self.co_delivery = ''
        self.new_address_needed = ''
        self.delivery_deadline_date='today'
        self.delivery_status=''
        self.delivery_time=''
        self.delivery_date=''



    def __str__(self):
        return f"Package: {self.id} {self.weight_kg}\nDelivery Details: {self.street_address} {self.city}, {self.state}  {self.zip_code}   {self.delivery_deadline_time} {self.delivery_truck} \nSpecial Notes:  {self.special_notes} {self.delayed_delivery_time} {self.co_delivery}  {self.new_address_needed}"