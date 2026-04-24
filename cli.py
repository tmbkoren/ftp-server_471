import sys
import socket
from common import BUFFER_SIZE, send_line, recv_line


def open_data_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))  # ephemeral port
    sock.listen(1)
    port = sock.getsockname()[1]
    return sock, port


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

            cmd = command.split()[0].lower()


            if cmd == "test":
                listener, data_port = open_data_listener()

                try:
                    send_line(client_socket, f"PORT {data_port}")
                    resp = recv_line(client_socket)
                    print(resp)

                    if not resp.startswith("OK"):
                        continue

                    send_line(client_socket, "TEST")

                    data_sock, _ = listener.accept()
                    data = data_sock.recv(BUFFER_SIZE)

                    print("Data channel received:",
                          data.decode("utf-8").strip())

                    data_sock.close()

                    print(recv_line(client_socket))  

                finally:
                    listener.close()


            elif cmd == "ls":
                listener, data_port = open_data_listener()

                try:
                    send_line(client_socket, f"PORT {data_port}")
                    resp = recv_line(client_socket)

                    if not resp.startswith("OK"):
                        print(resp)
                        continue

                    send_line(client_socket, "LS")

                    resp = recv_line(client_socket)
                    if not resp.startswith("OK"):
                        print(resp)
                        continue

                    data_sock, _ = listener.accept()

                    data = b""
                    while True:
                        chunk = data_sock.recv(BUFFER_SIZE)
                        if not chunk:
                            break
                        data += chunk

                    data_sock.close()

                    print(data.decode("utf-8"), end="")

                finally:
                    listener.close()


            elif cmd == "get":
                if len(command.split()) < 2:
                    print("Usage: get <filename>")
                    continue

                filename = " ".join(command.split()[1:])

                listener, data_port = open_data_listener()

                try:
                    send_line(client_socket, f"PORT {data_port}")
                    resp = recv_line(client_socket)

                    if not resp.startswith("OK"):
                        print(resp)
                        continue

                    send_line(client_socket, f"GET {filename}")

                    resp = recv_line(client_socket)
                    if not resp.startswith("OK"):
                        print(resp)
                        continue

                    size = int(resp.split()[1])

                    data_sock, _ = listener.accept()

                    received = 0
                    with open(filename, "wb") as f:
                        while received < size:
                            chunk = data_sock.recv(min(BUFFER_SIZE, size - received))
                            if not chunk:
                                break
                            f.write(chunk)
                            received += len(chunk)

                    data_sock.close()

                    print(f"{filename}: {received} bytes received")

                finally:
                    listener.close()

            elif cmd == "quit":
                send_line(client_socket, "QUIT")
                print(recv_line(client_socket))
                break


            else:
                send_line(client_socket, command)
                response = recv_line(client_socket)
                print(f"Server response: {response}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
