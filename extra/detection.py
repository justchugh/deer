import time
import datetime
import cv2
import shutil
import numpy as np
import torch
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Importing utilities and extra functionality from other modules
from extra.distance_measurement import distance_to_camera
from extra.model_load import scale_coords
from extra.log_detection import update_detection_log
from utils.augmentations import letterbox
from utils.general import check_img_size, non_max_suppression

# Classes for which we want to count detections
CLASS_ORDER = ["person", "dog", "deer", "rabbit", "raccoon", "squirrel"]

def create_filename(username, class_counts):
    # New date and time format for the filename
    timestamp = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")
    counts = ''.join(f"{class_counts.get(class_name, 0)}" for class_name in CLASS_ORDER)
    filename = f"IMG_{username.upper()}_{timestamp}_{counts}.jpg"
    return filename

class ImageHandler(FileSystemEventHandler):
    def __init__(self, model, device, opt, base_path):
        self.model = model
        self.device = device
        self.opt = opt
        self.base_path = Path(base_path)
        self.username = opt['username'].upper()

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            time.sleep(0.5)  # Delay for file stabilization
            try:
                self.process_image(event.src_path)
            except Exception as e:
                print(f"Error processing image {event.src_path}: {e}")

    def process_image(self, image_path):
        print(f"New image detected for processing: {image_path}")
        try:
            detect(image_path, self.model, self.device, self.opt, self.base_path)
        except Exception as e:
            print(f"Error during detection: {e}")

def detect(image_path, model, device, opt, base_path):
    username = opt['username'].upper()
    print("\n------------------------------------------------------------\n")
    print(f"Processing: {image_path}")
    img_time = time.time()

    im0 = cv2.imread(image_path)
    if im0 is None:
        print("Image could not be read, possibly corrupt file.")
        return

    imgsz = check_img_size(opt['img_size'], s=model.stride)
    im = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
    im = letterbox(im, imgsz, stride=model.stride, auto=True)[0]
    im = np.ascontiguousarray(im.transpose((2, 0, 1))[::-1])
    im = torch.from_numpy(im).to(device).float() / 255.0
    im = im[None]

    pred = model(im, augment=False, visualize=False)
    pred = non_max_suppression(pred, opt['conf_thres'], opt['iou_thres'], classes=None, agnostic=False, max_det=1000)

    class_names = [model.names[int(cls)] for det in pred for *xyxy, conf, cls in det]
    class_counts = {name: class_names.count(name) for name in set(class_names)}

    detected_dir = Path(opt['output'])
    dupes_dir = Path(opt['dupes'])
    logs_dir = Path(opt['logs'])
    dupes_dir.mkdir(parents=True, exist_ok=True)  # Ensure dupes directory exists

    if any(class_counts.values()):
        folder_path = detected_dir / "class"
    else:
        folder_path = detected_dir / "no_class"
        class_counts = {key: 0 for key in CLASS_ORDER}

    folder_path.mkdir(parents=True, exist_ok=True)
    filename = create_filename(username, class_counts)
    save_path = folder_path / filename

    # Draw bounding boxes and calculate distances
    if any(class_counts.values()):
        for det in pred:
            for *xyxy, conf, cls in det:
                class_name = model.names[int(cls)]
                # Calculate distance here
                width = xyxy[2] - xyxy[0]  # Assuming width is used for distance calculation
                distance = distance_to_camera(width)  # Add additional parameters if needed
                label = f"{class_name} {conf:.2f}, {distance:.2f} cm"
                cv2.rectangle(im0, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (147, 20, 255), 2)
                cv2.putText(im0, label, (int(xyxy[0]), int(xyxy[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imwrite(str(save_path), im0)
    print(f"Saved image at: {save_path}")

    # Log detection for all cases, including no detections
    if any(class_counts.values()):
        update_detection_log(username, distance, str(save_path), logs_dir)
    else:
        update_detection_log(username, 0, str(save_path),logs_dir)  # No detections, log distance as 0

    # Move the original image to the dupes directory
    shutil.move(image_path, dupes_dir / Path(image_path).name)
    print(f"Backup and logging completed for: {save_path}")
    print(f"Processing time for image: {time.time() - img_time:.6f} seconds")
    print("------------------------------------------------------------\n")


def start_monitoring(path, model, device, opt, exit_event, base_path):
    event_handler = ImageHandler(model, device, opt, base_path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while not exit_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Ensure 'model', 'device', 'opt', and 'base_path' are defined before calling this function
