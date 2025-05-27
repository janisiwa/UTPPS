import configparser
import csv
from datetime import datetime, timedelta

import Services
import Hash_Table


def open_store_packages():
    """
    Load package data from file and store packages in a Hash_Table.

    Uses a custom Hash_Table class to store package instances keyed by their ID.

    Returns:
        Hash_Table: A hash table containing all packages loaded from the file.
    """
    #use custom hash_table - Requirement A
    package_info_table = Hash_Table.Hash_Table()
    #load in the package file data
    package_data = Services.get_data_file('package_file')

    # make packages and store in hash table
    return make_packages(package_data,package_info_table)


def make_packages(data_lines, package_info_table: Hash_Table):
    """
    Create Package instances from raw data lines and add them to the Hash_Table.

    Args:
        data_lines (list): List of package data rows, each a list of string fields.
        package_info_table (Hash_Table): The hash table to store packages by ID.

    Returns:
        Hash_Table: The hash table populated with Package objects.
    """
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
                new_package.end_of_day=True
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

            # add pacakge to package info table, using my hash_table class
            package_info_table.add(new_package.id, new_package)


        except ValueError as e:
            print(f'{e.args[0]} A new package was not created.')

    return package_info_table


#lookup function (by package id) to return package components - Requirement B
def get_package(package_info_table: Hash_Table, package_id: int):
    """
    Retrieve a Package object from the Hash_Table by package ID.

    Args:
        package_info_table (Hash_Table): The Hash_Table containing packages.
        package_id (int): The unique package ID to look up.

    Returns:
        Package or None: The Package object if found, else None.
    """
    #use look-up function - Requirement B
    found_package = package_info_table.get(package_id)
    if found_package is None:
        return None
    else:
        return found_package


def package_status_all(package_info_table: Hash_Table, package_id=0, time: datetime = timedelta(0)):
    """
    Print and summarize the delivery status of packages at a given time.

    Args:
        package_info_table (Hash_Table): The hash table containing packages.
        package_id (int, optional): Specific package ID to query; 0 to query all packages. Defaults to 0.
        time (datetime, optional): The datetime to check status against. Defaults to timedelta(0).

    Returns:
        tuple: (delivered_count (int), total_packages (int)) reflecting how many packages were delivered by the time.
    """
    Services.print_line()
    package_list = None

    #get all packages
    if package_id == 0:
        summary_title = f'UTPPS Package Delivery Summary - All Packages at {time.strftime("%m-%d-%Y %I:%M %p")}'
        print(f'{summary_title:^220}')
        package_list = package_info_table.get_all()
    #get a specific package
    else:
        summary_title = f'UTPPS Package Delivery Summary for Package ID {package_id} at {time.strftime("%m-%d-%Y %I:%M %p")}'
        print(f'{summary_title:^220}')
        package_list = [package_info_table.get(package_id)]

    #if there is no package with that ID
    if package_list == [None]:
        print(f'No packages were found with package ID {package_id}.')

    #print package info
    delivered_count = 0
    for package_count, package in enumerate(sorted(package_list, key=lambda package: package.delivery_truck)):

        #print the status for each package based on the time
        Services.print_line()
        print(package.print_status(time))
        # track the number of packages that are delivered at the time
        if package.timed_status == 'Delivered':
            delivered_count += 1
        Services.print_line()
    #return number of packages delivered out of total packages at the time
    return delivered_count, package_count + 1


class Package:
    """
    Represents a delivery package with attributes for address, deadline, weight, notes,
    delivery status, and timing information.
    """

    __package_ids = set()

    def __init__(self, package_id: 'int'):
        """
        Initialize a Package instance and validate the uniqueness and type of package ID.

        Args:
            package_id (int): Unique identifier for the package.

        Raises:
            ValueError: If package_id is not an int or if the ID already exists.
        """
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
        self.delivery_status = ''
        self.delivery_end_datetime = None
        self.delivery_start_datetime = None
        self.delivery_deadline = None
        self.timed_status = ''
        self.end_of_day=False

    def get_address(self):
        """
        Get a string representing the package delivery address and ZIP code separated by a pipe.

        Returns:
            str: Concatenation of street address and ZIP code with a pipe separator.
        """
        address_zip = f'{self.street_address}|{self.zip_code}'
        return address_zip

    def print_status(self, time: datetime):
        """
        Get a formatted string describing the delivery status of the package at the specified time.

        Args:
            time (datetime): The time to evaluate the package's status.

        Returns:
            str: Formatted string with package ID, address, delivery status, and assigned truck info.
        """
        #use the time to retrieve the correct package status information

        #check for address change based on time
        if self.new_address_needed != 'No':
            try:
                new_address_needed_time = Services.convert_str_datetime('', self.new_address_needed)
                if new_address_needed_time <= time:
                    address_at_time = '410 S State St'
                    zip_at_time = '84111'
                else:
                    address_at_time = self.street_address
                    zip_at_time = self.zip_code
            except ValueError:
                new_address_needed_time = None
                address_at_time = self.street_address
                zip_at_time = self.zip_code
        else:
            address_at_time = self.street_address
            zip_at_time = self.zip_code

        #get delivery info based on time
        if self.delivery_end_datetime <= time:
            status_at_time = 'Delivered'
            delivery_endtime_at_time = self.delivery_end_datetime.strftime('%m-%d-%Y %I:%M %p')
            truck_at_time = f'Truck #{self.delivery_truck}'
        elif self.delivery_end_datetime > time > self.delivery_start_datetime:
            status_at_time = 'En route'
            delivery_endtime_at_time = ''
            truck_at_time = f'Truck #{self.delivery_truck}'
        elif self.delayed_delivery_time is not None and self.delayed_delivery_time > time:
            status_at_time = f'Delayed - expected to arrive at hub {self.delayed_delivery_time}'
            delivery_endtime_at_time = ''
            truck_at_time = ''
        else:
            status_at_time = 'At hub'
            delivery_endtime_at_time = ''
            truck_at_time = ''

        #temporarily store status at that time
        self.timed_status = status_at_time
        display_address = f'Delivery Address: {address_at_time} {self.city}, {self.state} {zip_at_time}'
        display_delivery_status = f'Delivery Status: {status_at_time} {delivery_endtime_at_time}'

        #display package weight and delivery deadline
        weight = f'Weight: {self.weight_kg} kg'
        deadline_eod=f'Delivery Deadline: (EOD) {self.delivery_deadline.strftime("%m-%d-%Y %I:%M %p")}'
        deadline_timed =f'Delivery Deadline: {self.delivery_deadline.strftime("%m-%d-%Y %I:%M %p")}'
        deadline = f'{deadline_eod if self.end_of_day else deadline_timed}'
        return f'Package ID: {self.id:<5}{weight:<15}{display_address:<90}{deadline:<50}{display_delivery_status:<50}{truck_at_time}'

    def __str__(self):
        """
        Get a string representation of the package with delivery address and status info.

        Returns:
            str: Formatted string with package ID, delivery address, delivery status, and assigned truck.
        """
        display_address = f'Delivery Address: {self.street_address} {self.city}, {self.state} {self.zip_code}'
        display_delivery_status = f'Delivery Status: {self.delivery_status} {self.delivery_end_datetime.strftime("%m-%d-%Y %I:%M %p")}'
        # display package weight and delivery deadline
        weight = f'Weight: {self.weight_kg} kg'
        deadline_eod = f'Delivery Deadline: (EOD) {self.delivery_deadline.strftime("%m-%d-%Y %I:%M %p")}'
        deadline_timed = f'Delivery Deadline: {self.delivery_deadline.strftime("%m-%d-%Y %I:%M %p")}'
        deadline = f'{deadline_eod if self.end_of_day else deadline_timed}'
        return f'Package ID: {self.id:<15}{weight:<20}{display_address:<90}{deadline:<50}{display_delivery_status:<50}Assigned Truck #{self.delivery_truck}'

