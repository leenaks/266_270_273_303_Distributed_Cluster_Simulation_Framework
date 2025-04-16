import os
import time
import requests

NODE_ID = os.environ.get("NODE_ID")
API_SERVER_URL = os.environ.get("API_SERVER_URL")

print("Starting node.py...")
print(f"NODE_ID = {NODE_ID}")
print(f"API_SERVER_URL = {API_SERVER_URL}")

if not NODE_ID or not API_SERVER_URL:
    print("NODE_ID or API_SERVER_URL not set!")
    exit(1)

while True:
    try:
        response = requests.post(f"{API_SERVER_URL}/heartbeat", json={"node_id": NODE_ID}, timeout=5)
        print(f"Heartbeat sent from node {NODE_ID}: {response.status_code} - {response.json()}")
    except Exception as e:
        print("Error sending heartbeat:", e)
    time.sleep(5)
