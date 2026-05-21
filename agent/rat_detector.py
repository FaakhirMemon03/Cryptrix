import psutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BLACKSET = {
    "anydesk.exe",
    "teamviewer.exe",
    "rustdesk.exe",
    "remotedesktop.exe",
    "chrome_remote_desktop.exe",
    "vncviewer.exe",
    "tightvnc.exe"
}

def get_running_rats():
    """Identifies running processes from the blacklist."""
    found_rats = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in BLACKSET:
                found_rats.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return found_rats

def kill_rats():
    """Kills any running processes found in the blacklist."""
    killed_count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in BLACKSET:
                logging.info(f"Killing RAT process: {proc.info['name']}")
                proc.kill()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return killed_count

if __name__ == "__main__":
    rats = get_running_rats()
    if rats:
        logging.warning(f"Detected RATs: {rats}")
        # kill_rats() # Commented out for safety during development
    else:
        logging.info("No common RATs detected.")
