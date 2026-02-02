import os
import re
import csv
import json

instance_log = {}
login_list = []

# Open the log file
with open('sample.log', 'r') as file:
    # Read each line
    for line in file:
        # Check if line contains "Failed password"
        if 'Failed password' in line:
            # Identify and track IP addresses
            match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            # If an IP address is found, store it
            if match:
                ip_address = match.group(0)
                # Tracks failed login attempts
                if ip_address in instance_log:
                    instance_log[ip_address] += 1
                else:
                    instance_log[ip_address] = 1
    # Prints output header
    print("Failed login attempts by IP:")
    # Prints failed login attempts and number of times for each address
    for ip_address in instance_log:
        print(f'{ip_address}: {instance_log[ip_address]}')
    # Prints total failed login attempts
    print(f'Total failed attempts: {sum(instance_log.values())}')
# Create exports directory if it doesn't exist
os.makedirs('exports', exist_ok=True)
# Writes to CSV
with open('exports/failed_logins.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['IP Address', 'Attempt Count']) # Writes header 
    for ip_address in instance_log:
        writer.writerow([ip_address, instance_log[ip_address]])  #Writes IP and failed attempts
# Writes to JSON
for ip_address in instance_log:
    login_list.append({"IP Address": ip_address, "Attempt Count": instance_log[ip_address]})
# Prepares data for JSON output
data = {
    "failed_logins": login_list,
    "total_attempts": sum(instance_log.values())
    }
# Writes the JSON output to a file
with open('exports/failed_logins.json', 'w') as file:
    json.dump(data, file, indent=4)