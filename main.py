
import socket
import os
import requests

def get_ip():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def check_port(ip, port):
    """Check if a specific port on a given IP address is open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        result = True
    except Exception:
        result = False
    finally:
        s.close()
    return result

def get_hostname(ip):
    """Get the hostname of a given IP address."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror as e:
        hostname = f"Unknown Host (Error: {e})"
    return hostname

def ping_ip(ip):
    """Ping an IP address to check its reachability."""
    response = os.system(f"ping -c 1 -W 1 {ip}" if os.name != 'nt' else f"ping -n 1 -w 1 {ip}")
    return response == 0

def get_public_ip():
    """Get the public IP address of the machine."""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
    except requests.RequestException:
        public_ip = "Could not retrieve public IP"
    return public_ip

def main():
    print("Welcome to the Network Utility App!")
    print("Please choose one of the following options:")
    print("1. Get Local IP Address")
    print("2. Check if a Port is Open on a Given IP Address")
    print("3. Get Hostname of a Given IP Address")
    print("4. Get Public IP Address")

    
    choice = input("Enter your choice (1, 2, 3, or 4): ")

    if choice == '1':
        local_ip = get_ip()
        print(f"Your local IP address is: {local_ip}")
    elif choice == '2':
        target_ip = input("Enter the IP address to check: ")
        target_port = int(input("Enter the port number to check: "))
        if check_port(target_ip, target_port):
            print(f"Port {target_port} on {target_ip} is open.")
        else:
            print(f"Port {target_port} on {target_ip} is closed.")
    elif choice == '3':
        target_ip = input("Enter the IP address to find the hostname: ")
        if ping_ip(target_ip):
            hostname = get_hostname(target_ip)
            print(f"The hostname for IP address {target_ip} is: {hostname}")
        else:
            print(f"IP address {target_ip} is not reachable.")
        retry = input("Do you want to try another IP address? (yes/no): ").strip().lower()
        while retry == 'yes':
            target_ip = input("Enter the IP address to find the hostname: ")
            if ping_ip(target_ip):
                hostname = get_hostname(target_ip)
                print(f"The hostname for IP address {target_ip} is: {hostname}")
            else:
                print(f"IP address {target_ip} is not reachable.")
            retry = input("Do you want to try another IP address? (yes/no): ").strip().lower()
        if retry == 'no':
            print("Exiting the program.")
    elif choice == '4':
        public_ip = get_public_ip()
        print(f"Your public IP address is: {public_ip}")
    else:
        print("Invalid choice. Please run the program again and enter either 1, 2, or 3.")

if __name__ == "__main__":
    main()
