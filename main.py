import Hash_Table
from Services import DataServices
from Truck import Truck


def load_trucks(truck_list, distance_list, address_list, package_info_table):
    pass


def run_UTPPS():
    # store and retrieve package information
    package_info_table = Hash_Table.Hash_Table()

    # helper to read files
    data_service = DataServices()

    #at the beginning of the day, setup data
    open_store_packages(data_service,package_info_table)
    distance_list = open_store_distances(data_service)
    address_list = open_store_addresses(data_service)

    #create the empty trucks
    truck_list = open_store_trucks(data_service)

    load_trucks(truck_list,distance_list,address_list,package_info_table)  


def open_store_trucks(data_service):
    truck_list = []
    #read in the truck information from the config file
    number_of_trucks = int(data_service.get_config_info('truck_info','trucks_available').strip())
    package_max=int(data_service.get_config_info('truck_info','package_maximum'))
    driver_list = data_service.get_config_info('truck_info','truck_drivers_available').split(',')

    #create the trucks
    for i in range(number_of_trucks):
        truck=Truck(i+1,package_max,driver_list[i])
        truck_list.append(truck)
    return truck_list

def open_store_packages(data_service:DataServices, package_info_table:Hash_Table):
   #load in the package file data
    package_data = data_service.get_data_file('package_file')

    # make packages and store in hash table
    data_service.make_packages(package_data,package_info_table)

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




if __name__ == "__main__":
    run_UTPPS()