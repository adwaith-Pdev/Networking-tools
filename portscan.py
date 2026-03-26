import socket
from datetime import datetime

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode(errors="ignore")
        sock.close()
        return banner.strip()
    except:
        return None


def detect_os(ttl):
    # Very rough heuristic
    if ttl <= 64:
        return "Linux/Unix"
    elif ttl <= 128:
        return "Windows"
    else:
        return "Unknown"


def scan_ports(target, start_port, end_port):#here we initialise the starting and end port maybe default 1-1024
    print(f"\n🔍 Scanning {target}")
    print("-" * 60)

    try:
        target_ip = socket.gethostbyname(target)
    except:
        print("❌ Invalid target")
        return

    print(f"Target IP: {target_ip}")
    print(f"Started at: {datetime.now()}")
    print("-" * 60)

    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            banner = grab_banner(target_ip, port)

            print(f"\n✅ Port {port} OPEN")
            print(f"   Service: {service}")

            if banner:
                print(f"   Version Info: {banner[:100]}")
            else:
                print("   Version Info: Not detected")

            open_ports.append(port)

        sock.close()

    print("\n" + "-" * 60)
    print(f"Finished at: {datetime.now()}")
    print(f"Open ports: {open_ports}")

    # Basic OS Guess (not accurate like Nmap)
    try:
        ttl = socket.gethostbyname(target_ip)
        print("\n🧠 OS Guess: Very basic (not reliable)")
        print("sorry couldnt identify")
    except:
        pass


if __name__ == "__main__":
    target = input("Target (IP/domain): ")
    start = int(input("Start port: "))
    end = int(input("End port: "))

    scan_ports(target, start, end)
