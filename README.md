This script is a network diagnostic tool that retrieves and displays various details about the user's internet connection. 

![2](https://github.com/user-attachments/assets/ad900787-b60b-4745-b02f-bbc8a0793b23)

Installation:
```
git clone https://github.com/WhoamiGroot/Whats-IP
```
```
pip install speedtest-cli
```
or
```
easy_install speedtest-cli
```
```
pip install requests
```
```
pip install dnspython
```
Run the script:
```
Python3 whatsip.py
```

Here's a breakdown of its functionality:
Features

    Retrieves Public IP Address & ISP
        Uses https://ipinfo.io/json to fetch the public IP and ISP details.

    Finds Local IP Address
        Uses socket.gethostname() and socket.gethostbyname() to determine the local device's IP.

    Fetches DNS Server Information
        Uses dns.resolver.Resolver().nameservers to list the configured DNS servers.
        Queries ipinfo.io to determine the ISP of each DNS server.

    Performs an Internet Speed Test
        Uses the speedtest module to measure download and upload speeds.
        
![1](https://github.com/user-attachments/assets/bc603b3b-4887-4a38-810b-69c3eda520fe)

Example of output in JSON:

When run, the script will output a JSON response like this:
```
{
    "public_ip": {
        "ip": "192.168.1.1",
        "isp": "Some ISP"
    },
    "local_ip": "192.168.0.2",
    "dns_servers": [
        {
            "dns": "8.8.8.8",
            "isp": "Google"
        },
        {
            "dns": "8.8.4.4",
            "isp": "Google"
        }
    ],
    "internet_speed": {
        "download_speed": "50.00 Mbps",
        "upload_speed": "20.00 Mbps"
    }
}
```
