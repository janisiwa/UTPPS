#Janis Wint -- Student Number:012214215 -- WGU C950 -- Task II
import Hash_Table
import Truck
import Package
import Services

from datetime import datetime, timedelta

def read_required_string_as_time(prompt:str,usingtime:bool=False):
    #verify the input is not empty
    input_string = input(prompt)
    if input_string.strip() =='':
        print('A value is required.')
        return read_required_string_as_time(prompt, usingtime)

    # allow user to cancel using a q character
    if input_string.strip().lower() =='q':
        return False

    if usingtime:
        #very input is a time
        try:
            return Services.convert_str_datetime('',input_string)

        except ValueError:
            return read_required_string_as_time('Incorrect time format. Enter a time of day (eg 8:05 am or 4:30 pm):',True)
    else:
        #verify package ID is an integer
        try:
            return int(input_string)

        except ValueError:
            return read_required_string_as_time('Incorrect id format. Enter a package ID (eg 23):',False)




def run_UTPPS():

    #at the beginning of the day, setup data
    package_info_table =Package.open_store_packages()
    distance_list = Truck.open_store_distances()
    address_list = Truck.open_store_addresses()

    #create the empty trucks
    truck_list = Truck.open_store_trucks()

    #place the packages into the trucks
    Truck.load_trucks(truck_list,distance_list,address_list,package_info_table)

    #start deliveries
    for truck in truck_list:
        truck.deliver_packages()

    #run the UTPPS user interface
    UTPPS_UI(truck_list,package_info_table)




def create_menu():
    #display options to the user in the command line interface
    print(f'{'--- Utah Private Parcel Service (UTPPS) ---':^220}')
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
                input_time = read_required_string_as_time('Enter a time of day (eg 8:05 am or 4:30 pm):',True)
                if input_time:
                    input_id = read_required_string_as_time('Enter a package ID (eg 23):', False)
                    if input_id:
                        Package.package_status_all(package_info_table,input_id, input_time)
                        Services.print_new_section()
                    else:
                        print('Not able to show a summary. Please try again.')
                else:
                    print('Not able to show a summary. Please try again.')
            case '2':
                input_time = read_required_string_as_time('Enter a time of day (eg 8:05 am or 4:30 pm):', True)
                if input_time:
                    delivered_count, total_count=Package.package_status_all(package_info_table,0,input_time)
                    # display cumulative all package summary
                    Services.print_line()
                    print(f'Delivered Packages: {delivered_count} Total Packages: {total_count}')
                    Services.print_new_section()
                else:
                    print('Not able to show a summary. Please try again.')


            case '3':
                Truck.total_miles_travelled(truck_list)
            case '4':
                exit_program()
            case _:
                print('Error - Enter a valid menu choice 1-4')


#run the program
if __name__ == '__main__':
    run_UTPPS()