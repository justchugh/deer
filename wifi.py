import subprocess
import time
import csv
import os
from datetime import datetime
import sys  # Import sys to handle command line arguments

# Construct the path for the file to store WiFi signal strength data
current_directory = os.path.dirname(os.path.realpath(__file__))
output_directory = os.path.join(current_directory, 'deer', 'logs')
output_file = os.path.join(output_directory, 'wifi_testing.csv')

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to determine if headers should be written
def should_write_headers(filename):
    return not os.path.exists(filename)

# Check if headers need to be written
write_headers = should_write_headers(output_file)

# Function to assess connection quality
def assess_connection_quality(link_quality):
    if link_quality is None:
        return 'Disconnected'  # Return 'Disconnected' if no link quality is available
    try:
        link_quality_num = int(link_quality.split('/')[0])
        if link_quality_num <= 35:
            return 'Poor'
        elif 36 <= link_quality_num <= 55:
            return 'Good'
        elif 56 <= link_quality_num <= 70:
            return 'Great'
    except ValueError:
        return 'Unknown'  # Return 'Unknown' if link quality is not in the expected format
    return 'Unknown'

# Function to get the current timestamp
def current_timestamp():
    return datetime.now().strftime('%m/%d/%y %H:%M:%S')

# Read duration from command line or set default
duration = 30  # Default duration of 30 seconds
if len(sys.argv) > 1:
    try:
        duration = int(sys.argv[1])
    except ValueError:
        print("Invalid input for duration. Using default 30 seconds.")

# Start capturing data
print(f"Starting data capture for {duration} seconds...")

# Capture data for specified duration
for i in range(duration):
    # Clear the screen
    print('\033c', end='')

    # Run iwconfig and capture output
    result = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
    output = result.stdout
    
    # Print the iwconfig output
    print(f"Capturing data point {i+1}...\n")
    print("iwconfig output:")
    print(output.strip())

    # Extract link quality and signal level
    link_quality = None
    signal_level = None
    for line in output.split('\n'):
        if 'Link Quality' in line:
            parts = line.split()
            link_quality = parts[1].split('=')[1]
        if 'Signal level' in line:
            parts = line.split()
            if '=' in parts[-1]:
                signal_level = parts[-1].split('=')[1]

    # Get current timestamp
    timestamp = current_timestamp()
    
    # Assess connection quality
    connection_quality = assess_connection_quality(link_quality)
    
    # Open file for appending or writing
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if write_headers:
            writer.writerow(['timestamp', 'link_quality', 'signal_level', 'connection_quality'])
            write_headers = False  # Ensure headers are not written again

        # Write data to CSV
        writer.writerow([timestamp, link_quality, signal_level, connection_quality])

    # Print extracted values, data writing confirmation, and connection quality
    print(f"Extracted Link Quality: {link_quality}, Signal Level: {signal_level}")
    print(f"Data written: {timestamp}, {link_quality}, {signal_level}, {connection_quality}\n")
    print(f"Connection Quality: {connection_quality}")

    # Wait for 1 second before capturing the next data point
    time.sleep(1)

print(f"\n\nData capture completed. Data saved to {output_file}\n")
