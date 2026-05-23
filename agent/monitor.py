import time
import logging
import json
import os
try:
    from agent.commands import shutdown_system, restart_system, lock_workstation, block_input, unblock_input, factory_reset
    from agent.lockdown import initiate_lockdown
    from agent.security_utils import capture_webcam, get_network_info
    from agent.rat_detector import get_running_rats
    from agent.warning_ui import show_warning
except (ImportError, ModuleNotFoundError):
    from commands import shutdown_system, restart_system, lock_workstation, block_input, unblock_input, factory_reset
    from lockdown import initiate_lockdown
    from security_utils import capture_webcam, get_network_info
    from rat_detector import get_running_rats
    from warning_ui import show_warning
import threading
import uuid
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CryptrixAgent:
    def __init__(self):
        self.is_running = True
        # Automatically get the MAC address as a unique device ID
        self.device_id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                                   for ele in range(0, 8*6, 8)][::-1])
        
        # Get local IP
        try:
            self.local_ip = socket.gethostbyname(socket.gethostname())
        except:
            self.local_ip = "Unknown"

        logging.info(f"Cryptrix Agent Initialized.")
        logging.info(f"DEVICE ID (MAC): {self.device_id}")
        logging.info(f"LOCAL IP: {self.local_ip}")

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
            # Show warning screen in a separate thread
            threading.Thread(target=show_warning, daemon=True).start()
            initiate_lockdown(shutdown_after=params.get("shutdown", False))
        elif action == "FACTORY_RESET":
            factory_reset()
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
        # Get the directory where the executable or script is located
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            # If running from monitor.py, move up one level to reach project root
            if os.path.basename(base_path) == 'agent':
                base_path = os.path.dirname(base_path)

        cmd_file = os.path.join(base_path, "incoming_cmd.json")
        
        logging.info(f"Agent is listening for remote commands in: {base_path}")
        logging.info(f"Command file path: {cmd_file}")
        
        try:
            while self.is_running:
                if os.path.exists(cmd_file):
                    try:
                        # Add a small delay to ensure file is fully written
                        time.sleep(0.1) 
                        with open(cmd_file, 'r') as f:
                            cmd_data = json.load(f)
                        self.process_command(cmd_data)
                        
                        # Use a retry loop for deletion in case of file locks
                        for _ in range(3):
                            try:
                                os.remove(cmd_file)
                                break
                            except:
                                time.sleep(0.5)
                    except Exception as e:
                        logging.error(f"Failed to process command file: {e}")
                
                time.sleep(2) # Polling interval
        except KeyboardInterrupt:
            logging.info("Agent stopped by user.")

if __name__ == "__main__":
    agent = CryptrixAgent()
    agent.run()

