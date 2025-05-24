#Janis Wint -- Student Number:012214215 -- WGU C950 -- Task II
import Hash_Table
import Truck
import Package
import Services

from datetime import datetime, timedelta

def read_required_string_as_time(prompt: str, usingtime: bool = False):
    """Prompts the user for a required input string and converts it to a time or integer.

    Recursively asks the user until valid input is provided or user cancels with 'q'.

    Args:
        prompt (str): The message displayed to the user.
        usingtime (bool, optional): If True, input is expected to be a time string;
            if False, input is expected to be an integer package ID. Defaults to False.

    Returns:
        datetime.datetime or int or bool: Returns a datetime object if usingtime is True,
            an integer if usingtime is False, or False if the user cancels input with 'q'.
    """
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
    """Runs the main Utah Private Parcel Service (UTPPS) program workflow.

    Initializes data, loads trucks with packages, delivers packages,
    and starts the user interface.
    """
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
    """Displays the command line menu options for the UTPPS system."""
    #display options to the user in the command line interface
    print(f'{"--- Utah Private Parcel Service (UTPPS) ---":^220}')
    print('Delivery Status Options:')
    print('1. View a package status using package id')
    print('2. View status of all packages')
    print('3. View end of day summary with total miles travelled for all trucks')
    print('4. Exit')
    print('Select [1-4]: ')





def exit_program():
    """Prints a message indicating the program is exiting. Last execution before the program ends."""
    Services.print_line()
    print('Exiting the UTPPS System! Bye!')
    Services.print_line()

def UTPPS_UI(truck_list, package_info_table):
    """Runs the UTPPS command line user interface for package and delivery status queries.

    Args:
        truck_list (list): List of Truck objects representing delivery trucks.
        package_info_table (Hash_Table): Hash_Table storing package information.
    """
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
                #display end of day summary
                end_of_day = Services.convert_str_datetime('','5:00 pm')
                delivered_count, total_count = Package.package_status_all(package_info_table, 0, end_of_day)
                # display cumulative all package summary
                Services.print_line()
                print(f'Delivered Packages: {delivered_count} Total Packages: {total_count}')
                Services.print_new_section()
                Truck.total_miles_travelled(truck_list)
            case '4':
                exit_program()
            case _:
                print('Error - Enter a valid menu choice 1-4')


#run the program
if __name__ == '__main__':
    run_UTPPS()
