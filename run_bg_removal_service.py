#!/usr/bin/env python3
"""
Robust Background Removal Service Runner
Ensures the service stays running and restarts on failure
"""

import subprocess
import time
import requests
import sys
import os
import signal

def kill_existing_service():
    """Kill any existing background removal service"""
    try:
        result = subprocess.run(['pgrep', '-f', 'background_removal_service.py'], 
                              capture_output=True, text=True)
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"Killed existing process: {pid}")
                except:
                    pass
    except:
        pass

def start_service():
    """Start the background removal service"""
    env = os.environ.copy()
    env['PORT'] = '5001'
    
    process = subprocess.Popen(
        ['python3', 'background_removal_service.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return process

def check_health():
    """Check if service is healthy"""
    try:
        response = requests.get('http://localhost:5001/health', timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("Starting Background Removal Service Manager...")
    
    # Kill any existing service
    kill_existing_service()
    time.sleep(1)
    
    while True:
        print("\n[INFO] Starting background removal service...")
        process = start_service()
        
        # Wait for service to start
        time.sleep(3)
        
        # Check if service is healthy
        if check_health():
            print("[SUCCESS] Background removal service is running on port 5001")
        else:
            print("[WARNING] Service started but health check failed")
        
        # Monitor the service
        while process.poll() is None:
            time.sleep(5)
            if not check_health():
                print("[ERROR] Health check failed, restarting service...")
                process.kill()
                break
        
        if process.poll() is not None:
            print(f"[ERROR] Service crashed with code {process.poll()}")
            print("[INFO] Restarting in 2 seconds...")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down service manager...")
        kill_existing_service()
        sys.exit(0)