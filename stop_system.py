import subprocess
import os
import signal

def stop_main():
    try:
        # Retrieve all PIDs of processes matching the pattern
        processes = subprocess.check_output(["pgrep", "-f", "python main.py"]).decode().strip().split()
        for pid in processes:
            # Check if the process is a Python process to avoid stopping the shell
            cmd_line = subprocess.check_output(["ps", "-p", pid, "-o", "cmd"]).decode()
            if 'python main.py' in cmd_line:
                os.kill(int(pid), signal.SIGTERM)  # Kill the process
                print(f"Stopped process with PID: {pid}")
    except subprocess.CalledProcessError:
        print("main.py is not running or could not be stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    stop_main()
