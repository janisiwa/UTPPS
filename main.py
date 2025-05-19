import Hash_Table
from Services import DataServices
import Truck
import Package

from datetime import datetime


def run_UTPPS():
    # store and retrieve package information


    # helper to read files
    data_service = DataServices()

    #at the beginning of the day, setup data
    package_info_table =Package.open_store_packages(data_service)
    distance_list = Truck.open_store_distances(data_service)
    address_list = Truck.open_store_addresses(data_service)

    #create the empty trucks
    truck_list = Truck.open_store_trucks(data_service)

    #place the packages into the trucks
    Truck.load_trucks(data_service,truck_list,distance_list,address_list,package_info_table)

    #start deliveries 2 trucks at a time
    for truck in truck_list:
        print(f'Truck {truck.id}: packages:{truck.packages_not_delivered} \n departure time:{truck.departure_time}')







if __name__ == '__main__':
    run_UTPPS()