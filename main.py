#Janis Wint Student Number:012214215 WGU C950
import Hash_Table
from Services import DataServices
import Truck
import Package
import Services

from datetime import datetime, timedelta

def read_required_string_as_time(prompt):
    #verify the input is not empty
    input_string = input(prompt)
    while input_string.strip() =='':
        print('A value is required.')
        input_string = input(prompt)
    # allow user to cancel using a q character
    if input_string.strip() =='q':
        return False
    #very input is a time
    try:
        input_time = datetime.strptime(input_string, '%I:%M %p')
        return input_time
    except ValueError:
        print('Incorrect time format.')
        read_required_string_as_time('Enter a time of day (eg 8:05 am or 4:30 pm):')
        return False




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




def create_menu():
    #display options to the user in the command line interface
    print(f'{'Utah Private Parcel Service (UTPPS)':^220}\n\n')
    print('Delivery Status Options:')
    print('1. View a package status using package id')
    print('2. View status of all packages')
    print('3. View total miles travelled for all trucks')
    print('4. Exit')
    print('Select [1-4]: ')







def exit_program():
    Services. print_line()
    print('Exiting the UTPPS System! Bye!')
    Services.print_line()

def UTPPS_UI(truck_list,package_info_table):


    menu_choice = ''
    while menu_choice != '4':
        create_menu()
        menu_choice = input('').strip()

        match menu_choice.strip():
            case '1':
                input_time = read_required_string_as_time('Enter a time of day (eg 8:05 am or 4:30 pm):')
                if input_time:
                    Package.package_status_all(package_info_table,2, input_time)
                    Services.print_new_section()
            case '2':
                Package.package_status_all(package_info_table)
                # display cumulative all package summary
                Services.print_line()
                print(f'Total Packages Delivered: {package_info_table.size}')
                Services.print_new_section()

            case '3':
                truck_list[-1].total_miles_travelled(truck_list)
            case '4':
                exit_program()
            case _:
                print('Error - Enter a valid menu choice 1-4')



if __name__ == '__main__':
    run_UTPPS()