#Janis Wint Student Number:012214215 WGU C950
import Hash_Table
from Services import DataServices
import Truck
import Package

from datetime import datetime


def run_UTPPS():
    # helper utility to read data files, calculate distances and convert datetimes
    data_service = DataServices()

    #at the beginning of the day, setup data
    package_info_table =Package.open_store_packages(data_service)
    distance_list = Truck.open_store_distances(data_service)
    address_list = Truck.open_store_addresses(data_service)

    #create the empty trucks
    truck_list = Truck.open_store_trucks(data_service)

    #place the packages into the trucks
    Truck.load_trucks(data_service,truck_list,distance_list,address_list,package_info_table)

    #start deliveries
    for truck in truck_list:
        truck.deliver_packages()
        print(f'Truck #:{truck.id} Total Distance: {truck.trip_distance:.2f} Start Time: {truck.departure_time} Return Time: {truck.return_time}')









if __name__ == '__main__':
    run_UTPPS()