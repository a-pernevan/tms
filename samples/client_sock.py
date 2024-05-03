import socket

def send_message():
    host = '192.168.200.179'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            message = input("Enter a message: ")
            s.sendall(message.encode())

if __name__ == "__main__":
    send_message()