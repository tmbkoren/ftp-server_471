import sys
import socket
from common import send_line, recv_line, recv_exact


def main():
    if len(sys.argv) != 3:
        print("Usage: python cli.py <server> <port>")
        sys.exit(1)

    server = sys.argv[1]
    port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server, port))

    print("Connected to server. Type 'quit' to exit.")

    try:
        while True:
            command = input("ftp> ").strip()

            if not command:
                continue

            send_line(client_socket, command)

            if command.lower() == "quit":
                print(recv_line(client_socket))
                break
            if command.split()[0].lower() == "ls":
                response = recv_line(client_socket)
                if response and response.startswith("OK"):
                    parts = response.split()

                    if len(parts) > 1:
                        size = int(parts[1])    
                        data = recv_exact(client_socket, size)
                        print(data.decode("utf-8"), end="")
                    else:
                        print(f"Server response: {response}")
                else:
                    print(f"Error from server: {response}")
            else:
                response = recv_line(client_socket)
                print(f"Server response: {response}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
