import time
import logging
from commands import lock_workstation, block_input, disable_wifi, shutdown_system
from rat_detector import kill_rats

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initiate_lockdown(shutdown_after=False):
    """
    Executes a series of emergency security measures:
    1. Disables Wi-Fi
    2. Kills known RATs
    3. Blocks keyboard/mouse input
    4. Locks the workstation
    5. (Optional) Shuts down the system
    """
    logging.warning("!!! PANIC MODE INITIATED !!!")
    
    try:
        # 1. Disable Internet
        logging.info("Disabling Wi-Fi...")
        disable_wifi()
        
        # 2. Kill RATs
        logging.info("Terminating remote access tools...")
        killed = kill_rats()
        logging.info(f"Killed {killed} RAT processes.")
        
        # 3. Lock Workstation
        logging.info("Locking workstation...")
        lock_workstation()
        
        # 4. Block Input
        logging.info("Blocking keyboard/mouse input...")
        block_input()
        
        if shutdown_after:
            logging.info("Shutdown scheduled in 5 seconds...")
            time.sleep(5)
            shutdown_system()
            
    except Exception as e:
        logging.error(f"Error during lockdown execution: {e}")

if __name__ == "__main__":
    # Test lockdown (be careful running this!)
    # initiate_lockdown()
    pass
