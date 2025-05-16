import Hash_Table
import Package
from Services import PackageDataServices


def runUTPPS():
    #store and retrieve package information
    package_info_table =  Hash_Table.Hash_Table()

    #load in package data from file
    package_data_service = PackageDataServices()
    package_data = package_data_service.get_package_data()

    #make packages and store in hash table
    package_data_service.make_packages(package_data, package_info_table)
    package_2 = package_info_table.get(39)

    print(package_2)
if __name__ == "__main__":
    runUTPPS()