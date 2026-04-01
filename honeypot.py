import socket
import threading
import csv
import os
from datetime import datetime

HOST = "0.0.0.0"
PORTS = [22, 80, 443, 8080]

FAKE_BANNERS = {
    22: "SSH-2.0-OpenSSH_7.9p1 Ubuntu-10\n",
    80: "HTTP/1.1 200 OK\nServer: Apache/2.4.41\n\n",
    443: "HTTPS Secure Connection Established\n",
    8080: "Welcome to our secure service!\n"
}

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "connections.csv")

# Create log file with headers if it dont exkst yet
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'ip', 'port', 'data', 'username', 'password'])

def log_connection(addr, port, data="", username="", password=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, addr[0], port, data, username, password])

def handle_connection(conn, addr, port):
    print(f"[!] Connection from {addr} on port {port}")

    try:
        # this basically sends fake banners 
        banner = FAKE_BANNERS.get(port, "Welcome!\n")
        conn.sendall(banner.encode())

        
        try:
            data = conn.recv(1024).decode(errors='ignore')
        except:
            data = ""

        # Simulate login prompt for ssh like services
        conn.sendall(b"Username: ")
        username = conn.recv(1024).decode(errors='ignore').strip()

        conn.sendall(b"Password: ")
        password = conn.recv(1024).decode(errors='ignore').strip()

        print(f"[CREDS] {addr[0]} -> {username}:{password}")

        # Log everything
        log_connection(addr, port, data, username, password)

        # Fake response
        conn.sendall(b"Login incorrect\n")

    except Exception as e:
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
            threading.Thread(
                target=handle_connection,
                args=(conn, addr, port),
                daemon=True
            ).start()

def main():
    for port in PORTS:
        threading.Thread(
            target=start_honeypot_on_port,
            args=(port,),
            daemon=True
        ).start()

    # Keepinf main thread alive
    while True:
        pass

if __name__ == "__main__":
    main()
