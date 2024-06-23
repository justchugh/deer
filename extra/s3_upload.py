'''
from s3_upload_new import s3_upload_new

local_directory = 'path to the captured/detected images whichever you want'
bucket_name = 'umbc-raspi-bckt'
s3_folder = 'rpi1'

upload_to_s3(local_directory, bucket_name, s3_folder)
time.sleep(300)
'''
local_directory='/home/rpi3/Downloads/deer_deterrant/deer/detected'
bucket_name='umbc-raspi-bckt'
s3_folder='rpi2_p2'
csv_log_path='/home/rpi3/Downloads/deer_deterrant/deer/logs/detections_log_latest.csv'

import os
import boto3
import csv

TRACKING_FILE = os.path.join(local_directory, '/home/rpi3/Downloads/deer_deterrant/deer/logs/track.txt')

def list_files_to_upload():
    """
    Reads a tracking file to determine which files have already been uploaded.
    """
    uploaded_files = set()
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as file:
            uploaded_files = {line.strip() for line in file}
    return uploaded_files

def upload_to_s3(local_directory, 
                 bucket_name, 
                 s3_folder, 
                 csv_log_path):
    # Initialize the S3 client securely
    s3 = boto3.client('s3', aws_access_key_id='aws_access_key_id', aws_secret_access_key='aws_secret_access_key')
    uploaded_files = list_files_to_upload()
    #s3 = boto3.client('s3')
    # Read the CSV and prepare for re-writing
    
    for file_name in os.listdir(local_directory):
        file_path = os.path.join(local_directory, file_name)
        if file_name not in uploaded_files and os.path.isfile(file_path):
            s3_path = f"{s3_folder}/{file_name}"
            s3.upload_file(file_path, bucket_name, s3_path)
            print(f"Uploaded {file_name} to S3 at {s3_path}.")
            with open(TRACKING_FILE, 'a') as file:
                file.write(file_name + '\n')
                
                
    with open(csv_log_path, mode='r+', newline='') as file:
        reader = csv.DictReader(file)
        entries = list(reader)
        
        updated_entries = []

        # Process each row and prepare update
        for row in entries:
            if row['check_upload'] == 'not uploaded' and os.path.exists(row['Image_Path']):
                s3_path = f"{s3_folder}/{os.path.basename(row['Image_Path'])}"
                s3.upload_file(row['Image_Path'], bucket_name, s3_path)
                print(f"File '{row['Image_Path']}' uploaded to S3 at '{s3_path}'.")
                row['check_upload'] = 'uploaded'
            updated_entries.append(row)
        print("images uploaded")
        # Go back to the start of the file to rewrite it
        file.seek(0)
        file.truncate()  # Clear the file
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(updated_entries)  # Write all the updated rows back to the file

upload_to_s3(local_directory,bucket_name,s3_folder,csv_log_path)

