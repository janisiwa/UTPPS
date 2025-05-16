import Hash_Table
import Package
from Services import DataServices


def runUTPPS():
    #store and retrieve package information
    package_info_table =  Hash_Table.Hash_Table()

    #load in package data from file
    data_service = DataServices()
    package_data = data_service.get_data('package_file')

    #make packages and store in hash table
    data_service.make_packages(package_data, package_info_table)

    #load in distance data from file
    distance_data = data_service.get_data('distance_file')

    #load in address data from file
    address_data = data_service.get_data('address_file')


if __name__ == "__main__":
    runUTPPS()