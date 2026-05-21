import os
import ctypes
import platform

def shutdown_system():
    """Shuts down the system immediately."""
    if platform.system() == "Windows":
        os.system("shutdown /s /t 0")
    else:
        os.system("shutdown -h now")

def restart_system():
    """Restarts the system immediately."""
    if platform.system() == "Windows":
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot")

def lock_workstation():
    """Locks the Windows workstation."""
    if platform.system() == "Windows":
        ctypes.windll.user32.LockWorkStation()
    else:
        # For Linux (GNOME)
        os.system("gnome-screensaver-command -l")

def disable_wifi():
    """Disables the Wi-Fi interface (Windows specific)."""
    if platform.system() == "Windows":
        os.system('netsh interface set interface "Wi-Fi" disable')

def enable_wifi():
    """Enables the Wi-Fi interface (Windows specific)."""
    if platform.system() == "Windows":
        os.system('netsh interface set interface "Wi-Fi" enable')

def block_input(duration=None):
    """Blocks keyboard and mouse input (Requires Admin)."""
    if platform.system() == "Windows":
        ctypes.windll.user32.BlockInput(True)
        if duration:
            import time
            time.sleep(duration)
            ctypes.windll.user32.BlockInput(False)

def unblock_input():
    """Unblocks keyboard and mouse input."""
    if platform.system() == "Windows":
        ctypes.windll.user32.BlockInput(False)

def factory_reset():
    """Initiates a Windows Factory Reset (DANGEROUS)."""
    if platform.system() == "Windows":
        # This opens the factory reset wizard
        os.system("systemreset --factoryreset")
    else:
        logging.error("Factory reset only implemented for Windows.")
