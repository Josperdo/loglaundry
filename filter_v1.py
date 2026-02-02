import re

instance_log = {}

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
    # Prints failed login attempts and number of times each respective IP failed
    for ip_address in instance_log:
        print(f'{ip_address}: {instance_log[ip_address]}')
    # Prints total failed login attempts
    print(f'Total failed attempts: {sum(instance_log.values())}')