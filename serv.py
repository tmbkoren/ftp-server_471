import os
import sys
import socket
from common import send_line, recv_line


def main():
    if len(sys.argv) != 2:
        print("Usage: python serv.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(1)

    print(f"Server listening on port {port}...")

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")

        client_ip = addr[0]
        pending_data_port = None

        try:
            while True:
                line = recv_line(connection_socket)
                if line is None:
                    break

                print(f"Received: {line}")

                parts = line.split()
                cmd = parts[0].lower()

                if cmd == "quit":
                    send_line(connection_socket, "BYE")
                    break

                elif cmd == "port":
                    if len(parts) != 2:
                        send_line(connection_socket, "ERROR Invalid PORT")
                        continue

                    try:
                        pending_data_port = int(parts[1])
                        send_line(connection_socket, "OK")
                    except:
                        send_line(connection_socket, "ERROR Invalid port")

                elif cmd == "test":
                    if pending_data_port is None:
                        send_line(connection_socket, "ERROR No data port set")
                        continue

                    try:
                        data_sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
                        data_sock.connect((client_ip, pending_data_port))

                        message = "hello from server\n".encode("utf-8")
                        data_sock.sendall(message)

                        data_sock.close()
                        send_line(connection_socket, "OK")

                        print("SUCCESS: test data connection")

                    except Exception as e:
                        send_line(connection_socket, f"ERROR {str(e)}")
                        print(f"FAILURE: test - {str(e)}")

                    pending_data_port = None  # reset

                elif cmd == "ls":
                    if pending_data_port is None:
                        send_line(connection_socket, "ERROR No data port set")
                        continue
                    try:
                        files = os.listdir(".")
                        listing = "\n".join(files) + "\n"
                        data = listing.encode("utf-8")

                        send_line(connection_socket, f"OK")
                        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data_sock.connect((client_ip, pending_data_port))
                        data_sock.sendall(data)
                        data_sock.close()

                        print("SUCCESS: ls")

                    except Exception as e:
                        send_line(connection_socket, f"ERROR: {str(e)}")
                        print(f"ERROR: ls - {str(e)}")

                elif cmd == "get":
                    if len(parts) < 2:
                        send_line(connection_socket, "ERROR Missing filename")
                        continue

                    if pending_data_port is None:
                        send_line(connection_socket, "ERROR No data port set")
                        continue

                    filename = " ".join(parts[1:])

                    if not os.path.isfile(filename):
                        send_line(connection_socket, "ERROR File not found")
                        pending_data_port = None
                        print(f"FAILURE: get {filename}")
                        continue

                    try:
                        size = os.path.getsize(filename)
                        send_line(connection_socket, f"OK {size}")

                        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data_sock.connect((client_ip, pending_data_port))

                        with open(filename, "rb") as f:
                            while True:
                                chunk = f.read(4096)
                                if not chunk:
                                    break
                                data_sock.sendall(chunk)

                        data_sock.close()

                        print(f"SUCCESS: get {filename} ({size} bytes)")

                    except Exception as e:
                        send_line(connection_socket, f"ERROR {str(e)}")
                        print(f"FAILURE: get {filename} - {str(e)}")

                    pending_data_port = None

                else:
                    send_line(connection_socket, "ERROR: Unknown command")
                    print(f"ERROR: Unknown command '{cmd}'")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Client disconnected")
            connection_socket.close()


if __name__ == "__main__":
    main()
