import re

# Open the log file
x = 0
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
            # Print output
                print(f'Failed login from: {ip_address}')
            # Add to total count
            x += 1
    print(f'Total failed attempts: {x}')  
    