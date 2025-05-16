import os
import configparser
import csv
import Package

class DataServices:

    def get_data(self, file_type:str):
        # get package data file location from application config file
        config = configparser.ConfigParser()
        config_file_path = os.path.join(os.getcwd(), 'app_config.ini')
        config.read(config_file_path)
        package_file_location = config.get('data_sources', file_type)

        # open the file
        data = open(package_file_location, encoding='utf-8-sig')
        csv_reader = csv.reader(data)
        data_lines = list(csv_reader)
        return data_lines

    def make_packages(self, data_lines,package_info_table):
        # load in the package components
        for data_line in data_lines:
            # assign the unique id to the new package
            temp_id = int(data_line[0])
            try:
                new_package = Package.Package(temp_id,package_info_table)
                new_package.street_address = data_line[1]
                new_package.city = data_line[2]
                new_package.state = data_line[3]
                new_package.zip_code = data_line[4]
                new_package.delivery_deadline_time = data_line[5]
                new_package.weight_kg = data_line[6]
                new_package.special_notes = data_line[7]
                new_package.delayed_delivery_time = data_line[8]
                new_package.delivery_truck = data_line[9]
                new_package.co_delivery = data_line[10]
                new_package.new_address_needed = data_line[11]

                # add pacakge to package info table
                package_info_table.add(new_package.id, new_package)

            except ValueError as e:
                print(f"{e.args[0]} A new package was not created.")
