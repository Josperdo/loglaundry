# Open the log file
x = 0
with open('sample.log', 'r') as file:
    # Read each line
    for line in file:
        # Check if line contains "Failed password"
        if 'Failed password' in line:
            # Print output
            print(line.strip())
            # Add to total count
            x += 1
    print(f'Total failed attempts: {x}')  
    