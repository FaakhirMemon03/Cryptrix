import cv2
import requests
import socket
import logging
import datetime
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def capture_webcam(filename=None):
    """Captures a snapshot from the primary webcam."""
    if filename is None:
        filename = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Could not open webcam.")
        return None
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
        logging.info(f"Webcam snapshot saved to {filename}")
        cap.release()
        return filename
    else:
        logging.error("Failed to capture image from webcam.")
        cap.release()
        return None

def get_network_info():
    """Retrieves current IP and location estimation via IP."""
    info = {}
    try:
        # Get local IP
        hostname = socket.gethostname()
        info['local_ip'] = socket.gethostbyname(hostname)
        
        # Get public IP and location
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            data = response.json()
            info['public_ip'] = data.get('ip')
            info['city'] = data.get('city')
            info['region'] = data.get('region')
            info['country'] = data.get('country_name')
            info['org'] = data.get('org')
        else:
            info['public_ip'] = "Could not retrieve"
            
    except Exception as e:
        logging.error(f"Error retrieving network info: {e}")
        info['error'] = str(e)
        
    return info

if __name__ == "__main__":
    # print(get_network_info())
    # capture_webcam()
    pass
