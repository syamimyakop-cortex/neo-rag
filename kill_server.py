import os
import subprocess

def kill_port(port):
    print(f"Looking for process on port {port}...")
    try:
        cmd = f"netstat -ano | findstr :{port}"
        output = subprocess.check_output(cmd, shell=True).decode()
        lines = output.strip().split('\n')
        killed = False
        for line in lines:
            if "LISTENING" in line:
                parts = line.split()
                pid = parts[-1]
                print(f"Found PID {pid}. Killing...")
                os.system(f"taskkill /F /PID {pid}")
                killed = True
        if not killed:
            print("No process found on port 8000.")
    except subprocess.CalledProcessError:
        print("No process found on port 8000.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kill_port(8000)
