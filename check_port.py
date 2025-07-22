import socket

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout to ensure the check is quick
    result = sock.connect_ex((host, port))
    sock.close()
    
    return result == 0

HOST = "localhost"
PORT = 8000

if check_port(HOST, PORT):
    print(f"The FastAPI application on port {PORT} is up and running.")
else:
    print(f"The FastAPI application on port {PORT} is not responding.")
