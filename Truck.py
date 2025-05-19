from Services import DataServices
import Hash_Table

def load_trucks(data_service:DataServices,truck_list:list, distance_list:list, address_list:dict, package_info_table:Hash_Table):

    for i, truck in enumerate(truck_list):
        #when loading the first truck, set up the services for all trucks
        if truck.trucks_data_service is None:
            truck.trucks_data_service=data_service
            truck.trucks_distance_list=distance_list
            truck.trucks_address_list=address_list
            truck.trucks_package_info_table=package_info_table

        # get the packages for that truck
        truck_package_list = data_service.get_config_info('truck_info', 'packages_'+str(i)).split(',')
        #use an algorithm to determine the route order
        truck.packages_not_delivered=optimized_route(truck_package_list)
        #set the delivery starting time
        truck.departure_time=data_service.convert_str_datetime('',data_service.get_config_info('truck_info', 'start_delivery_'+str(i)))
        #check packages against constraints
        truck.validate_packages()



def optimized_route(truck_package_list):
    #use nearest neighbor to reorder the packages
    return truck_package_list

def open_store_trucks(data_service):
    truck_list = []
    #read in the truck information from the config file
    number_of_trucks = data_service.get_config_info('truck_info','trucks_available').strip()
    if number_of_trucks.isdigit():
        number_of_trucks = int(number_of_trucks)
    package_max=data_service.get_config_info('truck_info','package_maximum')
    if package_max.isdigit():
        package_max = int(package_max)
    driver_list = data_service.get_config_info('truck_info','truck_drivers_available').split(',')

    #check for sufficient number of drivers
    driver_shortage = int(number_of_trucks)-len(driver_list)
    if driver_shortage > 0:
        driver_available=0
        for short_driver in range(driver_shortage):
            driver_list.append(driver_list[driver_available])
            if driver_available <len(driver_list)-1:
                driver_available+=1
            else:driver_available=0

    #create the trucks
    for i in range(number_of_trucks):
        truck=Truck(i+1,package_max,driver_list[i])
        truck_list.append(truck)
    return truck_list



def open_store_distances(data_service:DataServices):
    # load in distance data from file
    distance_data = list(data_service.get_data_file('distance_file'))
    return distance_data

def open_store_addresses(data_service:DataServices):
    # load in address data from file
    address_data_lines = list(data_service.get_data_file('address_file'))

    # store data using the address|zip as the key in the Python dictionary
    # will use .get method to get position of the address within the distance data list
    address_data = {address_zip: values for address_zip, *values in address_data_lines}
    return address_data

class Truck:
    #class level variable
    __truck_id=set()
    trucks_data_service=None
    trucks_distance_list=None
    trucks_address_list=None
    trucks_package_info_table=None


    def __init__(self, truck_id:'int',package_max:'int',driver=''):
        # ensure unique id
        if truck_id in Truck.__truck_id:
            raise ValueError(f'Truck with ID {truck_id} already exists.', truck_id)
        elif not type(truck_id) is int:
            raise ValueError(f'Truck with ID {truck_id} is not an integer.', truck_id)

        self.id = truck_id
        self.__truck_id.add(truck_id)
        self.driver=driver
        self.status='at hub'
        self.packages_not_delivered =None
        self.departure_time=None
        self.return_time=None
        self.trip_distance=0
        self.package_maximum=package_max
        self.route=None
        self.clock=''

    def get_trucks_count(self):
        return len(Truck.__truck_id)

    def deliver_packages(self):
        #start the delivery clock
        self.status='en route'
        self.clock=self.departure_time

        #mark all packages on route
        for package_id in self.packages_not_delivered:
            package = self.trucks_package_info_table.get(int(package_id))
            package.delivery_status='en route'

        #start at the hub, set current stop as address 0
        current_stop=0
        for package_id in self.packages_not_delivered:
            package =self.trucks_package_info_table.get(int(package_id))
            next_stop_address=package.get_address()
            next_stop_list = self.trucks_address_list.get(next_stop_address)
            next_stop= int(next_stop_list[0])
            next_stop_distance = self.get_distance(current_stop, next_stop)
            next_stop_time = self.trucks_data_service.next_stop_time(self.clock,next_stop_distance)

            #update package
            package.delivery_status='delivered'
            package.delivery_datetime=next_stop_time

            #update clock and distance for the truck
            self.clock = next_stop_time
            self.trip_distance+= next_stop_distance

            #update deliver log

            current_stop=next_stop

        #return to hub
        next_stop_distance = self.get_distance(current_stop, 0)
        next_stop_time = self.trucks_data_service.next_stop_time(self.clock, next_stop_distance)
        self.clock=next_stop_time
        self.return_time=next_stop_time
        self.status='at hub'

    def get_distance(self,x:int,y:int):
        #look up the distance between to locations
        distance = self.trucks_distance_list[x][y]

        #reverse the locations if the distance is not found
        if distance =='':
            return self.get_distance(y,x)
        else:
            return float(distance)

    def validate_packages(self):
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

            if not package.delayed_delivery_time=='':
                package.delivery_status="delayed"
            else:
                package.delivery_status = 'at hub'