import math
import Services

import Hash_Table
import re
from datetime import datetime, timedelta

def load_trucks(truck_list:list, distance_list:list, address_list:dict, package_info_table:Hash_Table):
    """
    Initialize and load trucks with packages, distance data, address data, and package information.

    Args:
        truck_list (list): List of Truck objects to be loaded.
        distance_list (list): Distance matrix used by trucks.
        address_list (dict): Dictionary of address data keyed by address|zip.
        package_info_table (Hash_Table): Hash_Table containing package information.

    Returns:
        None
    """
    for i, truck in enumerate(truck_list):
        #when loading the first truck, set up the services for all trucks
        if truck.trucks_data_service is None:
            truck.trucks_distance_list=distance_list
            truck.trucks_address_list=address_list
            truck.trucks_package_info_table=package_info_table

        # get the packages for that truck
        truck_package_list = Services.get_config_info('truck_info', 'packages_'+str(i)).split(',')
        #load onto the truck without optimization
        truck.packages_not_delivered=truck_package_list
        #set the delivery starting time
        truck.departure_time=Services.convert_str_datetime('',Services.get_config_info('truck_info', 'start_delivery_'+str(i)))
        #check packages against constraints
        truck.validate_packages()

def open_store_trucks():
    """
    Create and return a list of Truck objects based on configuration.

    Reads configuration to determine the number of trucks, maximum packages per truck,
    and assigns drivers, including handling driver shortages by reassigning drivers.

    Returns:
        list: A list of initialized Truck objects.
    """
    truck_list = []
    #read in the truck information from the config file
    number_of_trucks = Services.get_config_info('truck_info','trucks_available').strip()
    if number_of_trucks.isdigit():
        number_of_trucks = int(number_of_trucks)
    package_max=Services.get_config_info('truck_info','package_maximum')
    if package_max.isdigit():
        package_max = int(package_max)
    driver_list = Services.get_config_info('truck_info','truck_drivers_available').split(',')

    #check for sufficient number of drivers
    driver_shortage = int(number_of_trucks)-len(driver_list)
    if driver_shortage > 0:
        driver_available=0
        for short_driver in range(driver_shortage):
            driver_list.append(f'{driver_list[driver_available]} - from Truck {driver_available+1}')
            if driver_available <len(driver_list)-1:
                driver_available+=1
            else:driver_available=0

    #create the trucks
    for i in range(number_of_trucks):
        truck=Truck(i+1,package_max,driver_list[i])
        truck_list.append(truck)
    return truck_list

def open_store_distances():
    """
    Load and return distance data from the configured distance file.

    Returns:
        list: A list containing rows of distance data.
    """
    # load in distance data from file
    distance_data = list(Services.get_data_file('distance_file'))
    return distance_data

def open_store_addresses():
    """
    Load and return address data as a dictionary from the configured address file.

    The dictionary keys are address|zip codes, and values are associated data fields.

    Returns:
        dict: Dictionary mapping address|zip keys to corresponding address data values.
    """
    # load in address data from file
    address_data_lines = list(Services.get_data_file('address_file'))

    # store data using the address|zip as the key in the Python dictionary
    # will use .get method to get position of the address within the distance data list
    address_data = {address_zip: values for address_zip, *values in address_data_lines}
    return address_data

def total_miles_travelled(truck_list):
    """
    Print a delivery summary including individual truck distances and times,
    as well as cumulative totals for miles travelled and delivery time.

    Args:
        truck_list (list): List of Truck objects to summarize.

    Returns:
        None
    """
    #display individual truck delivery miles and time
    Services.print_line()
    print(f'{"UTPPS Truck Delivery Summary":^220}')
    Services.print_line()
    for truck in truck_list:
        print(f'Truck #:{truck.id}{" ":<15}Total Distance: {truck.trip_distance:.2g} mi{" ":<15}Start Time: {truck.departure_time.strftime("%m-%d-%Y %I:%M %p")}{" ":<15}Return Time: {truck.return_time.strftime("%m-%d-%Y %I:%M %p")}{" ":<15}Delivery Duration: {truck.total_delivery_time}')
        Services.print_line()

    #display cumulative miles and time
    Services.print_line()
    print(f'Total Miles Travelled: {truck_list[-1].get_cumulative_distance():2g} mi')
    print(f'Total Delivery Time: {truck_list[-1].get_total_time()}')
    print(f'Last Delivery: {truck_list[-1].return_time.strftime("%m-%d-%Y %I:%M %p")}')
    Services.print_new_section()

class Truck:
    """
    Represents a delivery truck with packages, routes, and associated delivery information.

    Class Attributes:
        _truck_ids (dict): Tracks existing truck IDs and their return times.
        _trucks_cumulative_distance (float): Cumulative distance travelled by all trucks.
        _trucks_total_time (timedelta): Total delivery time for all trucks.
        trucks_data_service (NoneType): Placeholder for shared service data.
        trucks_distance_list (list): Shared distance matrix for trucks.
        trucks_address_list (dict): Shared address data for trucks.
        trucks_package_info_table (Hash_Table): Shared package info Hash_Table.

    Instance Attributes:
        id (int): Unique truck identifier.
        driver (str): Name or identifier of the driver.
        status (str): Current status of the truck (e.g., 'At hub', 'En route').
        packages_not_delivered (list): List of package IDs currently loaded on truck.
        departure_time (datetime): Start time of the truck's delivery route.
        return_time (datetime): Time truck returns to the hub.
        trip_distance (float): Total distance travelled by this truck.
        package_maximum (int): Maximum number of packages the truck can carry.
        route (list): Optimized delivery route.
        clock (datetime or timedelta): Current time tracker during delivery.
        total_delivery_time (timedelta): Duration of this truck's delivery route.
    """

    #class level variable
    _truck_ids={}
    _trucks_cumulative_distance=0
    _trucks_total_time=timedelta(0)
    trucks_data_service=None
    trucks_distance_list=None
    trucks_address_list=None
    trucks_package_info_table=None

    def __init__(self, truck_id:'int',package_max:'int',driver=''):
        """
        Initialize a Truck instance.

        Args:
            truck_id (int): Unique identifier for the truck.
            package_max (int): Maximum number of packages allowed on the truck.
            driver (str, optional): Driver's name or identifier. Defaults to ''.

        Raises:
            ValueError: If the truck_id is not unique or not an integer.
        """
        # ensure unique id
        if truck_id in Truck._truck_ids:
            raise ValueError(f'Truck with ID {truck_id} already exists.', truck_id)
        elif not type(truck_id) is int:
            raise ValueError(f'Truck with ID {truck_id} is not an integer.', truck_id)

        self.id = truck_id
        Truck._truck_ids.setdefault(int(truck_id), None)
        self.driver=driver
        self.status='At hub'
        self.packages_not_delivered =None
        self.departure_time=None
        self.return_time=None
        self.trip_distance=0
        self.package_maximum=package_max
        self.route=None
        self.clock=None
        self.total_delivery_time=timedelta(0)

    def get_trucks_count(self):
        """
        Get the total number of Truck instances created.

        Returns:
            int: Number of trucks instantiated.
        """
        return len(Truck._truck_ids)

    def deliver_packages(self):
        """
        Execute the delivery process for the truck.

        Handles delayed starts if driver is shared, updates package statuses,
        optimizes delivery route, calculates distances and delivery times,
        and updates truck status and cumulative statistics.

        Returns:
            None
        """
        #delay delivery start time if waiting on a driver
        if re.search(r'Truck',self.driver):
            #get the truck number
            delayed_truck_id = int(self.driver.split('Truck')[1].strip())

            #set this truck to start delivering after the delayed truck ends its delivery
            delayed_truck_return_time= Truck._truck_ids.get(delayed_truck_id)
            self.departure_time = timedelta(minutes=10) + delayed_truck_return_time

        #start the delivery clock
        self.status='en route'
        self.clock=self.departure_time

        #mark all packages on route
        for package_id in self.packages_not_delivered:
            package = self.trucks_package_info_table.get(int(package_id))
            package.delivery_status='en route'
            package.delivery_start_datetime=self.departure_time

            if package.new_address_needed=='Yes':
                if self.clock > Services.convert_str_datetime('', '10:20 AM'):
                    #update address on package
                    package.street_address='410 S State St'
                    package.zip_code='84111'


        #optimize the routing for efficient delivery
        self.packages_not_delivered =self.optimize_route(self.packages_not_delivered)

        #start at the hub, set current stop as address 0
        current_stop=0
        for package_id in self.packages_not_delivered:
            package =self.trucks_package_info_table.get(int(package_id))
            next_stop_address=package.get_address()
            next_stop_list = self.trucks_address_list.get(next_stop_address)
            next_stop= int(next_stop_list[0])
            next_stop_distance = self.get_distance(current_stop, next_stop)
            next_stop_time = Services.next_stop_time(self.clock, next_stop_distance)

            #update package
            package.delivery_status='delivered'
            package.delivery_end_datetime=next_stop_time

            #update clock and distance for the truck
            self.clock = next_stop_time
            self.trip_distance+= next_stop_distance

            #update cumulative distance for all trucks
            Truck._trucks_cumulative_distance += next_stop_distance

            current_stop=next_stop

        #return to hub
        next_stop_distance = self.get_distance(current_stop, 0)
        next_stop_time = Services.next_stop_time(self.clock, next_stop_distance)
        self.clock=next_stop_time

        self.return_time=next_stop_time
        Truck._truck_ids[self.id]=self.return_time
        self.total_delivery_time= self.return_time - self.departure_time
        Truck._trucks_total_time += self.total_delivery_time
        self.status='at hub'

    def get_distance(self,x:int,y:int):
        """
        Retrieve the distance between two locations based on indices.

        Args:
            x (int): Index of the first location.
            y (int): Index of the second location.

        Returns:
            float: Distance between the two locations.

        Notes:
            If distance is not found in the direct order, attempts to retrieve distance in reverse order using recursive call.
        """
        #look up the distance between to locations
        distance = self.trucks_distance_list[x][y]

        #reverse the locations if the distance is not found
        if distance =='':
            return self.get_distance(y,x)
        else:
            return float(distance)

    def validate_packages(self):
        """
        Validate that the packages loaded on the truck meet constraints.

        Checks that the number of packages does not exceed the maximum allowed,
        verifies package assignment to this truck, and updates package delivery statuses.

        Raises:
            ValueError: If the truck has more packages than allowed or if a package is assigned to a different truck.
        """
        #check packages against maximum load
        if len(self.packages_not_delivered)>self.package_maximum:
            raise ValueError(f'Truck has more than {self.package_maximum} packages.', len(self.packages_not_delivered))

        #check packages that are assigned to a specific truck
        for package_id in self.packages_not_delivered:
            package =self.trucks_package_info_table.get(int(package_id))

            if package.delivery_truck.isdigit():
                if not package.delivery_truck == self.id:
                    raise ValueError(f'Package {package.id} is not assigned to Truck {self.id}.', package.delivery_truck)
            else:
                package.delivery_truck = self.id

            if package.delayed_delivery_time is not None:
                package.delivery_status="delayed"
            else:
                package.delivery_status = 'at hub'


    def optimize_route(self, not_visited_package_list:list):
        """
        Optimize delivery route using nearest neighbor heuristic.

        Args:
            not_visited_package_list (list): List of package IDs to deliver.

        Returns:
            list: Optimized list of package IDs for delivery order.
        """
        #use the nearest neighbor heuristic to optimize delivery routing
        route = []
        current_location = 0
        not_visited = not_visited_package_list.copy()

        while not_visited:
            # Find the package closest to the current location
            closest_package = None
            closest_distance = math.inf

            for package_id in not_visited:
                package = self.trucks_package_info_table.get(int(package_id))
                address_key = package.get_address()
                address_index = int(self.trucks_address_list[address_key][0])
                distance = self.get_distance(current_location, address_index)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_package = package_id

            # Add the closest package to the route and remove it from not visited
            route.append(closest_package)
            current_location = int(self.trucks_address_list[self.trucks_package_info_table.get(int(closest_package)).get_address()][0])
            not_visited.remove(closest_package)

        return route

    @classmethod
    def get_cumulative_distance(cls):
        """
        Returns the total cumulative distance traveled by all trucks.

        Returns:
            float: The cumulative distance traveled by all trucks.
        """
        return Truck._trucks_cumulative_distance

    @classmethod
    def get_total_time(cls):
        """
        Returns the total delivery time accumulated by all trucks.

        Returns:
            datetime.timedelta: The total delivery time for all trucks.
        """
        return Truck._trucks_total_time