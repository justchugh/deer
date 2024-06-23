### MODEL LOADING & EXTRAS
'''
Loads the detection model using YOLOv5 framework, adjusting for the specified compute device (CPU or GPU).
Dynamically quantizes the model for optimized inference on CPU.
'''

import time
from pathlib import Path
import sys
import os
import threading
import argparse
import signal
import logging
import getpass

# Adjust the path to the root directory of YOLOv5
ROOT = Path("/usr/local/lib/python3.11/dist-packages/yolov5").resolve()
#ROOT = Path("/home/rpi3/Downloads/deer_deterrant/model")
#BASE_PATH = Path("/home/rpi3/Downloads/deer_deterrant")
sys.path.append(ROOT.as_posix())
start_time = time.time()

import torch
from models.common import DetectMultiBackend
from utils.torch_utils import select_device



def scale_coords(img1_shape, coords, img0_shape):
    """Scale coordinates from img1_shape to img0_shape."""
    gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = new / old
    coords[:, [0, 2]] -= (img1_shape[1] - img0_shape[1] * gain) / 2
    coords[:, [1, 3]] -= (img1_shape[0] - img0_shape[0] * gain) / 2
    coords[:, :4] /= gain
    coords[:, 0].clamp_(0, img0_shape[1])
    coords[:, 1].clamp_(0, img0_shape[0])
    coords[:, 2].clamp_(0, img0_shape[1])
    coords[:, 3].clamp_(0, img0_shape[0])
    return coords

def configure_parser(base_path):
    """Configure command line arguments."""
    parser = argparse.ArgumentParser(description="Detection Configuration")
    username = getpass.getuser()
    parser.add_argument('--username', type=str, default=username, help='Username of the person running the script')
    parser.add_argument('--weights', nargs='+', type=str, default=os.path.join(base_path, 'model', 'deer.pt'), help='model path(s)')
    parser.add_argument('--device', type=str, default='cpu', help="Compute device")
    parser.add_argument('--img-size', type=int, default=640, help="Inference image size")
    parser.add_argument('--conf-thres', type=float, default=0.25, help="Confidence threshold")
    parser.add_argument('--iou-thres', type=float, default=0.45, help="IoU threshold for NMS")
    parser.add_argument('--input', type=str, default=os.path.join(base_path, 'deer', 'captures'), help='input directory path')
    parser.add_argument('--output', type=str, default=os.path.join(base_path, 'deer', 'detected'), help='output folder')
    parser.add_argument('--dupes', type=str, default=os.path.join(base_path, 'deer', 'dupes'), help='duplicate images folder')
    parser.add_argument('--logs', type=str, default=os.path.join(base_path, 'deer', 'logs', 'detections_log_latest.csv'), help='logs folder')
    parser.add_argument('--view-img', action='store_true', help='Enable image viewing during capture')
    return parser.parse_args()

def handle_exit(exit_event, signal_lock, force=False):
    """Handle program exit gracefully or forcefully."""
    with signal_lock:
        if exit_event.is_set() and not force:
            print("Exit already in progress...")
            return
        print("Handling exit...")
        exit_event.set()
        if not force:
            threading.Timer(15, lambda: handle_exit(exit_event, signal_lock, True)).start()
        else:
            print("Force exiting program after timeout...")
            os._exit(1)

def setup_signal_handling(exit_event, signal_lock):
    """Set up signal handling for graceful program termination."""
    signal.signal(signal.SIGINT, lambda signum, frame: handle_exit(exit_event, signal_lock))

def load_model(opt):
    """Load and quantize the model."""
    global start_time
    try:
        print("Model Loading Started")
        # Accessing as a dictionary
        device = select_device(opt['device'])  # Changed from opt.device to opt['device']
        model = DetectMultiBackend(opt['weights'], device=device, dnn=False)
        model.eval()  # Set the model to evaluation mode
        model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
        
        prep_time = time.time() - start_time
        print(f"Model loaded in {prep_time:.6f} seconds")
        print("Model loaded successfully. Starting the capture and detection threads.")
        return model, device, prep_time

    except Exception as e:
        logging.error(f"Failed to load the model: {e}", exc_info=True)
        sys.exit("Exiting due to model loading failure.")
