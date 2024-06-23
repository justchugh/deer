import time
import threading
import subprocess
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
# or
os.environ['QT_QPA_PLATFORM'] = 'xcb'  # if 'xcb' is available


from extra.pc import start_capture_view, start_capture_no_view
from extra.model_load import load_model, handle_exit, configure_parser, setup_signal_handling
from extra.detection import start_monitoring
from extra.file_management import create_directories

# Global flag to control thread exit and a lock for signal handling
exit_event = threading.Event()
signal_lock = threading.Lock()

def main():
    base_path = "/home/rpi3/Downloads/deer_deterrant"
    sec = 5  # capture seconds
    create_directories(base_path)
    args = configure_parser(base_path)  # This returns a Namespace object from argparse

    # Convert Namespace to dictionary
    opt = vars(args)  
    print(type(opt))
    print(opt)

    setup_signal_handling(exit_event, signal_lock)
    model, device, _ = load_model(opt)  # Now pass opt as a dictionary

    if args.view_img:
        capture_thread = threading.Thread(target=start_capture_view, args=(args.input,))
    else:
        capture_thread = threading.Thread(target=start_capture_no_view, args=(args.input, sec, exit_event,))

    threads = [
        capture_thread,
        threading.Thread(target=start_monitoring, args=(args.input, model, device, opt, exit_event, base_path))
    ]

    for thread in threads:
        thread.start()
    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.5)
    except:
        handle_exit(exit_event, signal_lock, force=True)

if __name__ == "__main__":
    main()
