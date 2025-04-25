import ssl
import socket

APHORISMS = [
    "Keep it simple.",
    "Be conservative in what you do.",
    "Assume the worst.",
    "Security is not a product, but a process."
]

def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=r"C:\Users\welcome\Downloads\csc2330_2025_a3\csc2330_2025_a3\backend\certs\backend.crt", keyfile=r"C:\Users\welcome\Downloads\csc2330_2025_a3\csc2330_2025_a3\backend\certs\backend.key")
    context.load_verify_locations(r"C:\Users\welcome\Downloads\csc2330_2025_a3\csc2330_2025_a3\backend\certs\ca.crt")
    context.verify_mode = ssl.CERT_OPTIONAL

    bindsocket = socket.socket()
    bindsocket.bind(('', 8443))
    bindsocket.listen(5)
    print("Backend TLS server listening on port 8443...")

    while True:
        newsocket, fromaddr = bindsocket.accept()
        with context.wrap_socket(newsocket, server_side=True) as conn:
            data = conn.recv(1024).decode()
            if "GET /aphorism" in data:
                response = APHORISMS[hash(fromaddr) % len(APHORISMS)]
                conn.sendall(response.encode())

if __name__ == "__main__":
    main()
