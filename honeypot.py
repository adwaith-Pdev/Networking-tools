import socket
import threading
import csv
import os
from datetime import datetime

# Configuration
HOST = "0.0.0.0"
PORTS = [22, 80, 443, 8080]

FAKE_BANNERS = {
    22: "SSH-2.0-OpenSSH_7.9p1 Ubuntu-10",
    80: "HTTP/1.1 200 OK\nServer: Apache/2.4.41",
    443: "HTTPS Secure Connection Established",
    8080: "Welcome to our super secure service!"
}

# Ensure logs folder exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "connections.csv")

# Initialize CSV file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'ip', 'port', 'data'])  # headers

def log_connection(addr, port, data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, addr[0], port, data])

def handle_connection(conn, addr, port):
    print(f"[!] Connection from {addr} on port {port}")
    try:
        data = conn.recv(1024).decode(errors='ignore')
        log_connection(addr, port, data)
        banner = FAKE_BANNERS.get(port, "Welcome!")
        conn.sendall(banner.encode())
    except:
        pass
    finally:
        conn.close()

def start_honeypot_on_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(5)
        print(f"[+] Listening on port {port} ...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_connection, args=(conn, addr, port)).start()

def main():
    for port in PORTS:
        threading.Thread(target=start_honeypot_on_port, args=(port,)).start()

if __name__ == "__main__":
    main()