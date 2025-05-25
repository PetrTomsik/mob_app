import socket

def get_local_ip():
    try:
        # Vytvoříme socket a připojíme se k veřejné adrese (bez odeslání dat)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip = s.getsockname()[0]
        s.close()
        print(f"IPV4 = {ip}")
        API_BASE_URL = f"http://{ip}:5000"
        return API_BASE_URL
    except:
        print(f"IPV4 ne ne ne= {ip}")
        return "127.0.0.1"  # fallback