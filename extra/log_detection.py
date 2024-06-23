import csv
import re
import datetime
import torch
import os

def update_detection_log(rpi_number, distance_cm, image_path, log_file_path):
    # Adjusted regex pattern to match the new date format and ensure proper capture
    pattern = re.compile(r'IMG_(RPI\d+)_(\d{8})_(\d{6})_(\d{6}).jpg')
    match = pattern.search(image_path)
    if match:
        rpi, date_str, time_str, counts_str = match.groups()
        # Properly convert date_str to datetime and format to 'MMDDYYYY' for processing
        date_obj = datetime.datetime.strptime(date_str, '%m%d%Y')
        # Convert time_str from 'HHMMSS' to 'HH:MM:SS' for display
        formatted_time_str = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
        timestamp = f"{date_obj.strftime('%m-%d-%Y')}_{formatted_time_str}"
        # Extract individual counts from the counts string
        person, dog, deer, rabbit, raccoon, squirrel = (int(count) for count in counts_str)
        short_image_path = f"{rpi}_{date_str}_{time_str}_{counts_str}.jpg"  # Use the same filename format
    else:
        short_image_path = os.path.basename(image_path)  # Fallback if regex doesn't match
        timestamp = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')  # Default timestamp if regex fails

    # Ensure the distance is formatted correctly
    if isinstance(distance_cm, torch.Tensor):
        distance_cm = round(distance_cm.item(), 2)  # Extract the numeric value from the tensor and round
    elif isinstance(distance_cm, (int, float)):
        distance_cm = round(distance_cm, 2)  # It's already a numeric type, just round it

    with open(log_file_path, 'a', newline='') as csvfile:
        fieldnames = ['RPI_No', 'Distance(cm)', 'Image_Path', 'Timestamp', 'Person', 'Dog', 'Deer', 'Rabbit', 'Raccoon', 'Squirrel', 'Check_Upload']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the CSV is empty and write headers if so
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'RPI_No': rpi_number.upper(),
            'Distance(cm)': distance_cm,
            'Image_Path': short_image_path,
            'Timestamp': timestamp,
            'Person': person,
            'Dog': dog,
            'Deer': deer,
            'Rabbit': rabbit,
            'Raccoon': raccoon,
            'Squirrel': squirrel,
            'Check_Upload': 'not uploaded'  # Hard-coded as 'not uploaded'
        })
        
#/home/rpi3/Downloads/deer_deterrant/deer/detected/no_class/img_rpi3_2024-06-18_20.45.28_0-0-0-0-0-0.jpg
