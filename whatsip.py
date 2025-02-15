import sys
import requests
import socket
import dns.resolver
import speedtest
import json
import time

print('''
█░█░█ █░█ ▄▀█ ▀█▀ █▀  █ █▀█
▀▄▀▄▀ █▀█ █▀█ ░█░ ▄█  █ █▀▀
Created by: WhoamiGroot                                               
'''
)

# Loading bar function
def loading_bar(duration, task_name):
    bar_length = 50  # Length of the loading bar
    sys.stdout.write(f"{task_name}: [")
    sys.stdout.flush()
    for i in range(bar_length + 1):
        progress = (i / bar_length) * 100
        bar = '#' * i + '-' * (bar_length - i)
        percentage = f"{progress:.2f}%"
        sys.stdout.write(f"\r{task_name}: [{bar}] {percentage}")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    print("] Done!")

# Function to get public IP info
def get_public_ip_info():
    try:
        loading_bar(2, "Fetching public IP")
        response = requests.get("https://ipinfo.io/json", timeout=10)
        response.raise_for_status()
        data = response.json()
        public_ip = data.get("ip", "N/A")  # Could be IPv4 or IPv6
        isp = data.get("org", "N/A")
        return public_ip, isp
    except requests.RequestException as e:
        return {"error": f"Error retrieving public IP info: {str(e)}"}

# Function to get local IP info
def get_local_ip():
    try:
        loading_bar(1, "Fetching local IP")
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        return {"error": f"Error retrieving local IP: {str(e)}"}

# Function to get DNS servers
def get_dns_servers():
    try:
        loading_bar(3, "Fetching DNS servers")
        resolvers = dns.resolver.Resolver().nameservers
        if not resolvers:
            return [{"dns": "No DNS servers found", "isp": "N/A"}]

        dns_info = []
        for resolver in resolvers:
            try:
                response = requests.get(f"https://ipinfo.io/{resolver}/json", timeout=10)
                response.raise_for_status()
                dns_data = response.json()
                dns_isp = dns_data.get("org", "Unknown ISP")
                dns_info.append({"dns": resolver, "isp": dns_isp})
            except requests.RequestException:
                dns_info.append({"dns": resolver, "isp": "Error retrieving ISP"})
        return dns_info
    except Exception as e:
        return [{"error": f"Error retrieving DNS servers: {str(e)}"}]

# Function to get internet speed
def get_internet_speed():
    try:
        loading_bar(5, "Measuring internet speed")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000  # Mbps
        return {"download_speed": f"{download_speed:.2f} Mbps", "upload_speed": f"{upload_speed:.2f} Mbps"}
    except speedtest.ConfigRetrievalError:
        return {"error": "Error retrieving speed: Config issue"}
    except Exception as e:
        return {"error": f"Speed test failed: {str(e)}"}

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() != "whatsmyip":
        print("Usage: python3 script.py whatsmyip")
        sys.exit(1)

    # Fetching public IP info
    public_ip_info = get_public_ip_info()

    # Fetching local IP info
    local_ip = get_local_ip()

    # Fetching DNS servers
    dns_servers = get_dns_servers()

    # Measuring internet speed
    speed_info = get_internet_speed()

    # Collecting all results
    result = {
        "public_ip": public_ip_info if isinstance(public_ip_info, dict) else {"ip": public_ip_info[0], "isp": public_ip_info[1]},
        "local_ip": local_ip if isinstance(local_ip, str) else {"error": local_ip.get("error")},
        "dns_servers": dns_servers,
        "internet_speed": speed_info if isinstance(speed_info, dict) else {"error": speed_info.get("error")}
    }

    # Output as JSON
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()

