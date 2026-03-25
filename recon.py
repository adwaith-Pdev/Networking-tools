import socket
import threading
import requests
from datetime import datetime

target = input("Target (IP/domain): ")
start_port = int(input("Start port: "))
end_port = int(input("End port: "))

open_ports = []
results = []
lock = threading.Lock()

COMMON_PATHS = ["/admin", "/login", "/dashboard", "/api", "/config", "/.env"]

VULN_PATTERNS = {
    "apache/2.2": "Outdated Apache",
    "php/5": "Outdated PHP",
    "vsftpd 2.3.4": "Backdoor vuln",
    "openssh_5": "Old SSH version"
}


def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").lower()
        s.close()
        return banner
    except:
        return ""


def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        if sock.connect_ex((ip, port)) == 0:
            banner = grab_banner(ip, port)

            with lock:
                open_ports.append(port)
                results.append(f"[+] Port {port} OPEN")

            print(f"[+] Port {port} OPEN")

            if banner:
                print(f"[i] {banner[:80]}")

                for vuln in VULN_PATTERNS:
                    if vuln in banner:
                        print(f"[!!!] {VULN_PATTERNS[vuln]}")
                        results.append(f"[VULN] Port {port}: {VULN_PATTERNS[vuln]}")

        sock.close()
    except:
        pass


def scan_http():
    print("\n[🌐] Web Analysis")

    for proto in ["http://", "https://"]:
        try:
            url = proto + target
            r = requests.get(url, timeout=3)

            print(f"[+] {url} -> {r.status_code}")
            results.append(f"{url} -> {r.status_code}")

            server = r.headers.get("Server", "")
            if server:
                print(f"[i] Server: {server}")
                results.append(f"Server: {server}")

                for vuln in VULN_PATTERNS:
                    if vuln in server.lower():
                        print(f"[!!!] {VULN_PATTERNS[vuln]}")
                        results.append(f"[VULN] {server}")

            # Scan common paths
            for path in COMMON_PATHS:
                try:
                    full_url = url + path
                    res = requests.get(full_url, timeout=2)

                    if res.status_code in [200, 403]:
                        print(f"[+] Found: {full_url}")
                        results.append(f"[FOUND] {full_url}")

                except:
                    pass

        except:
            continue


def save_report():
    filename = f"scan_{target}.txt"
    with open(filename, "w") as f:
        f.write("=== Scan Report ===\n")
        f.write(f"Target: {target}\n")
        f.write(f"Time: {datetime.now()}\n\n")

        for line in results:
            f.write(line + "\n")

    print(f"\n📁 Report saved as {filename}")


def main():
    try:
        ip = socket.gethostbyname(target)
    except:
        print("Invalid target")
        return

    print(f"\n🔍 Scanning {target} ({ip})...\n")

    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    scan_http()
    save_report()

    print("\n✅ Scan complete")
    print(f"Open ports: {open_ports}")


if __name__ == "__main__":
    main()