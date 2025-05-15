import Hash_Table
import Package

package_info_table =  Hash_Table.Hash_Table()
my_package =  Package.Package(5,package_info_table)
package_info_table_result = package_info_table.get(5)
package_info_table_results = package_info_table.get(5).street_address
print(f"Packing info: {my_package.street_address} \n Package table info: {package_info_table_results}")

