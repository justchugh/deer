import subprocess
import os
import signal

def stop_main():
    try:
        # Retrieve all PIDs of processes matching the pattern
        processes = subprocess.check_output(["pgrep", "-f", "python"]).decode().strip().split()
        for pid in processes:
            # Check if the process command line contains 'main.py'
            cmd_line = subprocess.check_output(["ps", "-p", pid, "-o", "cmd="]).decode().strip()
            if 'main.py' in cmd_line:
                os.kill(int(pid), signal.SIGTERM)  # Kill the process
                print(f"Stopped process with PID: {pid}")
    except subprocess.CalledProcessError:
        print("main.py is not running or could not be stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    stop_main()


'''


Basic usage:

bash

ps

Detailed list of all processes:

bash

ps aux

Search for a specific process (e.g., python):

bash

    ps aux | grep python

pgrep:
The pgrep command looks through the currently running processes and lists the process IDs which match the selection criteria.

    Find process IDs by name:

    bash

pgrep python

Find process IDs by name with full details:

bash

    pgrep -a python

top:
The top command provides a dynamic real-time view of the system's processes.

    Run top:

    bash

    top

    Press q to quit.








'''
