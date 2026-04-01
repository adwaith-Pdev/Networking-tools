 Networking Tools

A collection of Python-based cybersecurity tools for network scanning, vulnerability detection, and honeypot simulation.



 What This Repo Does

- Scans target systems for open ports
- Performs basic vulnerability detection
- Analyzes web servers and endpoints
- Simulates services to capture attacker behavior



Tools Included

Port Scanner & Vulnerability Detector

Features:

-  Multi-threaded port scanning
-  Banner grabbing for service detection
-  Pattern-based vulnerability identification
-  Web analysis (HTTP/HTTPS)
-  Common endpoint discovery ("/admin", "/login", etc.)
- Automatic report generation

Output includes:

- Open ports
- Service banners
- Potential vulnerabilities
- Discovered endpoints

Multi-Port Honeypot

Features:

- Listens on multiple ports ("22", "80", "443", "8080")
- Simulates real services (SSH, HTTP, etc.)
- Captures and logs incoming attacker data
- Multi-threaded connection handling
- CSV-based logging for analysis


🛠️ Tech Stack

- Python
- Socket Programming
- Threading
- HTTP Requests ("requests")
- Networking (TCP/IP)


Usage

 Run Scanner

python scanner.py

You will be prompted for:

- Target (IP/domain)
- Port range
  

Run Honeypot

python honeypot.py


 Output

Scanner

- Generates report file:

scan_<target>.txt

Includes:

- Open ports
- Vulnerabilities
- Web findings


Honeypot

- Logs stored in:

/logs/connections.csv

Includes:

- Timestamp
- IP address
- Port
- Captured data


⚠️ Disclaimer

This project is for educational and ethical purposes only.
Do not scan or interact with systems without proper authorization.


 Purpose

- Learn network scanning & security concepts
- Understand real-world attack patterns
- Build hands-on cybersecurity tools

 Author

Adwaith
Cybersecurity enthusiastic 

