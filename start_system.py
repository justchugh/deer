import subprocess
import sys
import time
import signal
import os

# Call stop_system.py before starting the main script
subprocess.call(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "stop_system.py")])


def start_main(duration=None, view_img=False):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to main.py
    main_py_path = os.path.join(script_dir, "main.py")
    
    # Determine the command based on the view_img flag
    command = f"python {main_py_path}"
    if view_img:
        command += " --view-img"

    # Start the main application
    process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    print(f"main.py is started with PGID {os.getpgid(process.pid)} {'for ' + str(duration) + ' seconds' if duration else 'indefinitely'}.")

    try:
        if duration:
            time.sleep(duration)
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print("main.py has been stopped after the specified duration.")
        else:
            process.wait()
    except KeyboardInterrupt:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        print("main.py has been interrupted and stopped.")

if __name__ == "__main__":
    view_img = False
    duration = None

    # Parse command line arguments
    for arg in sys.argv[1:]:  # Skip the first argument (the script name)
        if arg == 'vi':
            view_img = True
        else:
            try:
                duration = int(arg)  # Try to convert other arguments to duration
            except ValueError:
                print(f"Warning: Ignoring unrecognized argument {arg}. Use '-vi' for viewing image or provide duration in seconds.")

    start_main(duration, view_img)
