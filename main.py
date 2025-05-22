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

    #run the UTPPS user interface
    UTPPS_UI(truck_list,package_info_table)


def print_line():
    #decorative line for spacing in the UI
    print('-'*220)

def print_new_section():
    print('\n\n')

def create_menu():
    #display options to the user in the command line interface
    print(f'{'Utah Private Parcel Service (UTPPS)':^220}\n\n')
    print('Delivery Status Options:')
    print('1. View a package status using package id')
    print('2. View status of all packages')
    print('3. View total miles travelled for all trucks')
    print('4. Exit')
    print('Select [1-4]: ')


def package_status_by_id():
    print('One package')

def package_status_all():
    print('All packages')

def total_miles_travelled(truck_list):
    #display individual truck delivery miles and time
    print_line()
    print(f'{'Truck Delivery Summary':^220}')
    print_line()
    for truck in truck_list:
        print(f'Truck #:{truck.id}{' ':<15}Total Distance: {truck.trip_distance:.2f}{' ':<15}Start Time: {truck.departure_time}{' ':<15}Return Time: {truck.return_time}{' ':<15}Delivery Time: {truck.total_delivery_time}')
        print_line()

    #display cumulative miles and time
    print_line()
    print(f'Total Miles Travelled: {truck_list[-1].get_cumulative_distance()}')
    print(f'Total Delivery Time: {truck_list[-1].get_total_time()}')
    print(f'Last Delivery: {truck_list[-1].return_time}')
    print_new_section()

def exit_program():
    print_line()
    print('Exiting the UTPPS System! Bye!')
    print_line()

def UTPPS_UI(truck_list,package_info_table):


    menu_choice = ""
    while menu_choice != "4":
        create_menu()
        menu_choice = input("").strip()

        match menu_choice.strip():
            case "1":
                package_status_by_id()

            case "2":
                package_status_all()

            case "3":
                total_miles_travelled(truck_list)
            case "4":
                exit_program()
            case _:
                print("Error - Enter a valid menu choice 1-4")



if __name__ == '__main__':
    run_UTPPS()