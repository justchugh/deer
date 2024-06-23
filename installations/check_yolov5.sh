#!/bin/bash

# Define the path to the YOLOv5 directory
YOLOV5_PATH="/home/rpi2/Downloads/deer_deterrant/model/yolov5"

# Print the path being checked
echo "Checking the directory at $YOLOV5_PATH"

# List the contents of the YOLOv5 directory
echo "Listing contents of $YOLOV5_PATH:"
ls -l $YOLOV5_PATH

# Check if the models directory exists
echo "Checking for 'models' directory within the YOLOv5 path:"
ls -l $YOLOV5_PATH/models

# Attempt to import the necessary module using a Python command
echo "Testing Python import of the module:"
python3 -c "import sys; sys.path.append('$YOLOV5_PATH'); from models.common import DetectMultiBackend; print('Import successful!')"

# Check current PYTHONPATH environment variable
echo "Current PYTHONPATH:"
echo $PYTHONPATH

# Check permissions
echo "Checking permissions for $YOLOV5_PATH:"
ls -ld $YOLOV5_PATH
ls -ld $YOLOV5_PATH/models

