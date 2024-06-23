import subprocess
import sys
import time
import signal
import os

def start_main(duration=None, view_img=False):
    # Determine the command based on the view_img flag
    command = "python main.py"
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
        if arg == '-vi':
            view_img = True
        else:
            try:
                duration = int(arg)  # Try to convert other arguments to duration
            except ValueError:
                print(f"Warning: Ignoring unrecognized argument {arg}. Use '-vi' for viewing image or provide duration in seconds.")

    start_main(duration, view_img)
