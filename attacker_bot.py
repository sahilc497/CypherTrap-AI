import requests
import time
import random

BASE_URL = "http://localhost:8000"

ATTACKS = [
    {"path": "/db", "method": "POST", "data": {"query": "SELECT * FROM users"}},
    {"path": "/db", "method": "POST", "data": {"query": "SELECT password FROM accounts WHERE username='admin'"}},
    {"path": "/db", "method": "POST", "data": {"query": "DROP TABLE transactions"}},
    {"path": "/admin", "method": "GET", "data": None},
    {"path": "/login", "method": "POST", "data": {"username": "admin", "password": "' OR '1'='1"}},
    {"path": "/config", "method": "GET", "data": None},
    {"path": "/db", "method": "POST", "data": {"query": "SELECT * FROM system_logs WHERE level='CRITICAL'"}},
    {"path": "/api/v1/user", "method": "GET", "data": None},
]

print("🚀 Starting CypherTrap Attack Simulator...")
print("Press Ctrl+C to stop.")

try:
    while True:
        attack = random.choice(ATTACKS)
        url = f"{BASE_URL}{attack['path']}"
        
        try:
            if attack['method'] == "POST":
                response = requests.post(url, json=attack['data'], timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            print(f"[{time.strftime('%H:%M:%S')}] Triggered Trap: {attack['method']} {attack['path']} -> {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
            
        # Wait between 1 to 4 seconds for realistic jitter
        time.sleep(random.uniform(1, 4))

except KeyboardInterrupt:
    print("\n🛑 Simulator stopped.")
