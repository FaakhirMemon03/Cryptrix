import json
import time
import os

def send_test_command(action, params=None):
    """Creates a command file that the agent will pick up."""
    cmd = {
        "action": action,
        "params": params or {}
    }
    
    with open("incoming_cmd.json", "w") as f:
        json.dump(cmd, f)
    
    print(f"Command '{action}' placed in incoming_cmd.json")

if __name__ == "__main__":
    print("Cryptrix Simulation Trigger")
    print("1. GET_INFO (Network/IP)")
    print("2. SNAPSHOT (Webcam)")
    print("3. CHECK_RATS (Scan for RATs)")
    print("4. LOCK (Workstation Lock)")
    print("5. PANIC_MODE (Lockdown - CAUTION)")
    
    choice = input("Enter choice (1-5): ")
    
    if choice == '1':
        send_test_command("GET_INFO")
    elif choice == '2':
        send_test_command("SNAPSHOT")
    elif choice == '3':
        send_test_command("CHECK_RATS")
    elif choice == '4':
        send_test_command("LOCK")
    elif choice == '5':
        confirm = input("Are you sure? This will initiate lockdown. (y/n): ")
        if confirm.lower() == 'y':
            send_test_command("PANIC_MODE")
    else:
        print("Invalid choice.")
