import configparser
import csv

import Hash_Table


class Package:

    def __init__(self, package_id:'int',package_info_table:'Hash_Table'):
        # check for duplicate unique id
        if package_info_table.get(package_id):
            raise ValueError(f"Package with id {package_id} already exists")

        self.id = package_id




    def __str__(self):
        return f"Package: {self.id} {self.weight_kg}\nDelivery Details: {self.street_address} {self.city}, {self.state}  {self.zip_code}   {self.delivery_deadline_time} {self.delivery_truck} \nSpecial Notes:  {self.special_notes} {self.delayed_delivery_time} {self.co_delivery}  {self.new_address_needed}"