import sys
import requests
import socket
import dns.resolver
import speedtest
import json

print('''
█░█░█ █░█ ▄▀█ ▀█▀ █▀  █ █▀█
▀▄▀▄▀ █▀█ █▀█ ░█░ ▄█  █ █▀▀
Created by: WhoamiGroot                                               
'''
)

def get_public_ip_info():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=10)
        response.raise_for_status()
        data = response.json()
        public_ip = data.get("ip", "N/A")  # Could be IPv4 or IPv6
        isp = data.get("org", "N/A")
        return public_ip, isp
    except requests.RequestException as e:
        return {"error": f"Error retrieving public IP info: {str(e)}"}

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        return {"error": f"Error retrieving local IP: {str(e)}"}

def get_dns_servers():
    try:
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

def get_internet_speed():
    try:
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

    public_ip_info = get_public_ip_info()
    local_ip = get_local_ip()
    dns_servers = get_dns_servers()
    speed_info = get_internet_speed()

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

