import os
import boto3
import csv
import getpass


# AWS credentials should be managed securely
aws_access_key_id=''
aws_secret_access_key='' 
bucket_name = 'umbc-raspi-bckt'

user_name = getpass.getuser()
s3_folder = f'{user_name}_p2'

# Function to construct an absolute path based on the script's directory
def construct_path(relative_path):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dir_path, relative_path))

# Define paths using the function to ensure they are correctly resolved
local_directory = construct_path('../deer/detected/class')
csv_log_path = construct_path('../deer/logs/detections_log_latest.csv')
TRACKING_FILE = construct_path('../deer/logs/Track_AWS_upload.txt')



# Ensure the directory for the tracking file exists
os.makedirs(os.path.dirname(TRACKING_FILE), exist_ok=True)


def list_files_to_upload():
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as file:
            uploaded_files = {line.strip() for line in file}
    else:
        uploaded_files = set()
        open(TRACKING_FILE, 'w').close()  # Create the tracking file if it doesn't exist
    return uploaded_files

def upload_to_s3(local_directory, bucket_name, s3_folder, csv_log_path):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    print("Connection made with AWS.")
    uploaded_files = list_files_to_upload()
    total_uploaded = 0
    
    try:
        with open(csv_log_path, mode='r+', newline='') as file:
            reader = csv.DictReader(file)
            entries = list(reader)
            updated_entries = []
            
            print("Processing entries from CSV...")
            for row in entries:
                # Adjusting for the prefix 'IMG_' in the filename
                image_path = 'IMG_' + row['Image_Path']
                file_name = os.path.basename(image_path)
                file_path = os.path.join(local_directory, file_name)
                class_indicator = file_name.split('_')[4][:6]

                if '000000' not in class_indicator and file_name not in uploaded_files:
                    if os.path.isfile(file_path):
                        try:
                            s3_path = f"{s3_folder}/{file_name}"
                            s3.upload_file(file_path, bucket_name, s3_path)
                            print(f"Uploaded {file_name} to S3 at {s3_path}.")
                            row['Check_Upload'] = 'uploaded'
                            with open(TRACKING_FILE, 'a') as track_file:
                                track_file.write(file_name + '\n')
                            total_uploaded += 1
                        except Exception as e:
                            continue  # Fail silently and continue processing
                    else:
                        continue  # Fail silently and continue processing

                updated_entries.append(row)

            file.seek(0)
            file.truncate()
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_entries)
            print(f"Uploaded {total_uploaded} files successfully.")
    except Exception as e:
        print(f"Error processing the CSV file: {str(e)}")

upload_to_s3(local_directory, bucket_name, s3_folder, csv_log_path)
