
# Captures images with fps and also shows a countdown for time to save
# Saves a captured images

# from capture to saving of image

import cv2
import time
from concurrent.futures import ThreadPoolExecutor
import datetime
import threading
    
def save_image(img, save_path, timestamp):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    filename = f"{save_path}/img_{timestamp}.jpg"
    cv2.imwrite(filename, img)
    print(f"Saved image at: {filename}")

def capture_images_view(save_path, executor, save_interval=5):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height
    #save_path = "deer/all_cap"  # Path to save images
    last_save_time = time.time()
    fps_update_interval = 10
    frame_counter = 0
    last_time = time.time()
    fps = 0  # Initialize FPS value

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_counter += 1
            if frame_counter % fps_update_interval == 0:
                current_time = time.time()
                fps = fps_update_interval / (current_time - last_time)
                last_time = current_time

            # Display FPS on frame continuously
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Calculate and display the countdown for the next save
            
            if time.time() - last_save_time < save_interval:
                time_to_next_save = save_interval - (time.time() - last_save_time)
                countdown_text = f"Saving in: {int(time_to_next_save)} s"
                cv2.putText(frame, countdown_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            cv2.imshow('Video Stream', frame)  # Display every frame
            current_time = time.time()
            if current_time - last_save_time >= save_interval:
                # Submitting the save task to executor
                executor.submit(save_image, frame, save_path, current_time)
                last_save_time = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_capture_view(save_path):
    with ThreadPoolExecutor(max_workers=4) as executor:
        capture_images_view(save_path, executor)
        
        
        




def capture_images_no_view(save_path, save_interval, exit_event):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #save_path = "deer/all_cap"

    last_save_time = time.time()

    while not exit_event.is_set():
        if exit_event.is_set():
            break  # Check right before potentially blocking call
        ret, frame = cap.read()
        if ret:
            if exit_event.is_set():
                break  # Check right after potentially blocking call
            current_time = time.time()
            if current_time - last_save_time >= save_interval:
                save_image(frame, save_path, current_time)
                last_save_time = current_time
        else:
            print("Failed to capture frame")
            break

    cap.release()
    cv2.destroyAllWindows()


def start_capture_no_view(save_path, sec, exit_event):
    capture_images_no_view(save_path, sec, exit_event)



