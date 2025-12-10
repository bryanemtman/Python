# ARP Spoofing & MITM Network Utility Tool  
*A Python-based educational tool for ARP spoofing, NAT handling, IP forwarding, and raw ARP frame crafting.*

---

## Description

This script allows the user to:
- Select a local network interface, retrieving its MAC, IPv4, netmask, and gateway.
- Manipulate host forwarding settings, toggling kernel-level IP forwarding.
- Add or remove NAT masquerading iptables rules, necessary for MITM lab testing.
- Craft a raw ARP frame using Python sockets and inject it directly onto the wire.
- Spoof ARP packets for observation and protocol experimentation.
- The tool includes a safety cleanup system that automatically restores NAT and forwarding settings when the program ends or if the user force-terminates it with CTRL+C.

*I intentionally made tbis script with sockets instead of other modules so that I can learn more about the bottom level infrastructure of systems.*

## How It Works
1. Interface Discovery

- Using the netifaces library, the script enumerates all network interfaces and extracts:
  - Interface name
  - MAC address
  - IPv4 address
  - Netmask
  - Default gateway

2. IP Forwarding & NAT

- When performing MITM experiments, forwarding and NAT are often necessary.
  - Uses ```sysctl``` to toggle net.ipv4.ip_forward.
  - Uses ```iptables``` to apply / remove the POSTROUTING MASQUERADE rule.

3. ARP Request Crafting

- The script constructs a raw ARP request by assembling:
  - Ethernet header
  - ARP hardware/protocol info
  - Spoofed sender MAC & IP
  - Target IP
- Then sends it through a raw AF_PACKET socket on Linux.

4. Safety Cleanup

- Through atexit and signal, the script guarantees that whenever it exits:
  - NAT rules are removed
  - IP forwarding is disabled
  - System is returned to original state
  - Even if the user hits CTRL+C.

## Usage
1. Install dependencies
```
pip install netifaces
```
3. Run the script (Linux only)
```
sudo python3 arp_mitm.py
```
Raw packet transmission + iptables manipulation requires root privileges.

## Program Flow

You will be prompted to select a network interface:
```
[*] Available interfaces:
[0] lo
[1] eth0
[2] wlan0

Select interface (name or number):
```
After choosing one, the tool displays:
```
[!] Network Info:
{'gateway': '192.168.1.1', 'iface': 'eth0', 'mac': '08:00:27:aa:bb:cc', 'ip': '192.168.1.50', 'netmask': '255.255.255.0'}
```
Menu Options
```
1. Enable IP Forwarding
2. Disable IP Forwarding
3. Enable NAT
4. Disable NAT
5. Send ARP Request
0. Exit
```
ARP Injection Example

When choosing option 5:
```
--- ARP Packet Builder ---
Spoofed sender IP: 192.168.1.1
Target IP: 192.168.1.25
[+] ARP frame sent.
```

## Requirements

- Linux system (due to raw AF_PACKET + iptables)
- Python 3.8+
- netifaces library
- Root privileges

## Future Improvements

- Input validation for IPv4 addresses
- Scan network to list active hosts
- Optional ARP poisoning module (lab only)
- Packet capture mode to monitor ARP replies
- Integration with Scapy for more protocol options
- Logging system for analysis or auditing
