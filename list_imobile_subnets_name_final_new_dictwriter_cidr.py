#Import Necessary Python libraries to run script
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import csv

# Define credential variables to connect to network devices and device IP iteration for ssh connection
username = input('Enter your SSH username: ')
password = getpass()

with open('devices_file_iponly') as f:
    devices_list = f.read().splitlines()

imobile_subnets = list()

for devices in devices_list:
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }
# Exception management functions inc ase connection to device fails
    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

# Commands to be run on each device in 'devices_file_iponly' text file
    
    imobile_config = net_connect.send_command('show run int vlan 1241')
    hostname = net_connect.send_command('sh start | i hostname').split()[1]
    
    int_version = 0
    int_version = imobile_config.find('interface Vlan1241')
    resp = imobile_config.splitlines()
    ipaddr = 'ip address'
    if int_version  > 0:
       
        print(hostname)
        print ('iMobile Interface Vlan1241 found')
        for line in resp:
            if  ipaddr in line:
                line = line.replace('ip address ', '').replace(' 255.255.248.0' , '/21').replace(' 255.255.252.0' , '/22').replace(' 255.255.254.0' , '/23').replace(' 255.255.255.0' , '/24').replace(' 255.255.255.128' , '/25').replace(' 255.255.255.192' , '/26').replace(' 255.255.255.224' , '/27')
                print(f"*********************************\n{line}\n")
                break
    else:
        print(hostname)
        print ('Did not find iMobile Interface')
        line = 'Did not find iMobile Interface'    
    
    # Define Dictionary to write to csv file

    csvdict = {'hostname': hostname, 'CORE IP': devices, 'Vlan1241 Subnet': line.strip()}
    imobile_subnets.append(csvdict)


for imobile_subnet in imobile_subnets:
    print(imobile_subnet)

# write command output from dictionary to csv file

fields = ['hostname', 'CORE IP', 'Vlan1241 Subnet']

with open('iMobile_subnets.csv', 'w', newline='') as data:
    writer = csv.DictWriter(data, fieldnames = fields, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for imobile_subnet in imobile_subnets:
        writer.writerow(imobile_subnet)
  
