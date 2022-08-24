This script will pull iMobile IP Subnets associated with site names and dump the results on a spreadsheet 

To run the script:

1) Install Python 3.9 on your workstation
2) Change system env. to https://geek-university.com/python/add-python-to-the-windows-path/
3) Copy the following files to the same path on your workstaton:
	
* list_imobile_subnets_name_final_new_dictwriter_cidr.py
* devices_file_iponly

4) Add the list of of Core IP addresses to devices_file_iponly on per line.
5) Run the script from within the file path where the Script and IP address file reside.
6) A csv file will be generated on the same file path with the iMobile subnets
7) Add the CSV file to the Regional Team Sharepoint
8) delete the local csv file generated for next time you run the script.

