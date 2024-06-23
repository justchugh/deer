# sudo chmod 775 install.sh

#!/bin/bash

# Install OpenCV
echo "Installing OpenCV on Raspberry Pi"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3-opencv
echo "OpenCV Installation Complete!"


# Install PyTorch
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
sudo apt-get update
sudo apt-get -y install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
sudo -H pip3 install torch torchvision torchaudio
pip install "numpy<2"
echo "Congratulations! You've successfully installed PyTorch on your Raspberry Pi 64-bit OS"


# Install PyQt5 and LabelImg
sudo apt-get install pyqt5-dev-tools
sudo pip3 install labelimg
echo "Congratulations! You've successfully installed LabelImg on your Raspberry Pi 64-bit OS"


# Create directory and install YOLOv5
sudo pip3 install yolov5 -t /home/rpi2/deer_deterrant/model/yolov5
echo "Congratulations! You've successfully installed YOLOv5 on your Raspberry Pi 64-bit OS"


# Verify the installations
python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"
echo "---------------------------------------------------------------------------"
pyrcc5 --version
echo "---------------------------------------------------------------------------"
pip3 show yolov5
echo "---------------------------------------------------------------------------"


Camera Installations

ls /dev/video*
sudo apt-get install fswebcam
sudo apt-get install feh
# python3 cam_check.py

pip3 install watchdog


