import time
import logging
import json
import os
from .commands import shutdown_system, restart_system, lock_workstation, block_input, unblock_input
from .lockdown import initiate_lockdown
from .security_utils import capture_webcam, get_network_info
from .rat_detector import get_running_rats

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CryptrixAgent:
    def __init__(self):
        self.is_running = True
        self.device_id = "PC-AGENT-001" # Should be unique or from config
        logging.info(f"Cryptrix Agent {self.device_id} initialized.")

    def process_command(self, cmd_data):
        """Dispatches commands to appropriate modules."""
        action = cmd_data.get("action")
        params = cmd_data.get("params", {})
        
        logging.info(f"Received command: {action}")
        
        if action == "SHUTDOWN":
            shutdown_system()
        elif action == "RESTART":
            restart_system()
        elif action == "LOCK":
            lock_workstation()
        elif action == "BLOCK_INPUT":
            block_input(duration=params.get("duration"))
        elif action == "UNBLOCK_INPUT":
            unblock_input()
        elif action == "PANIC_MODE":
            initiate_lockdown(shutdown_after=params.get("shutdown", False))
        elif action == "SNAPSHOT":
            capture_webcam()
        elif action == "GET_INFO":
            info = get_network_info()
            logging.info(f"Network Info: {info}")
        elif action == "CHECK_RATS":
            rats = get_running_rats()
            if rats:
                logging.warning(f"RATs detected: {rats}")
            else:
                logging.info("No RATs detected.")
        else:
            logging.warning(f"Unknown action: {action}")

    def run(self):
        """Main loop: In a real app, this would be a Firebase/Socket listener."""
        logging.info("Agent is listening for remote commands...")
        
        # Simulation: check for a local file 'incoming_cmd.json'
        # In production, replace this with a real-time event listener
        cmd_file = "incoming_cmd.json"
        
        try:
            while self.is_running:
                if os.path.exists(cmd_file):
                    try:
                        with open(cmd_file, 'r') as f:
                            cmd_data = json.load(f)
                        self.process_command(cmd_data)
                        os.remove(cmd_file) # Process only once
                    except Exception as e:
                        logging.error(f"Failed to process command file: {e}")
                
                time.sleep(2) # Polling interval
        except KeyboardInterrupt:
            logging.info("Agent stopped by user.")

if __name__ == "__main__":
    agent = CryptrixAgent()
    agent.run()
