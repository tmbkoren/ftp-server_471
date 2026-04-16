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

        try:
            while True:
                line = recv_line(connection_socket)
                if line is None:
                    break  # client disconnected

                print(f"Received: {line}")

                parts = line.split()
                cmd = parts[0].lower()
                if cmd == "quit":
                    send_line(connection_socket, "BYE")
                    break
                
                elif cmd == "ls":
                    try:
                        files = os.listdir(".")
                        listing = "\n".join(files) + "\n"
                        data = listing.encode("utf-8")
                        send_line(connection_socket, f"OK {len(data)}")
                        connection_socket.sendall(data)
                        print("SUCCESS: ls")

                    except Exception as e:
                        send_line(connection_socket, f"ERROR: {str(e)}")
                        print(f"ERROR: ls - {str(e)}")

                else:
                    send_line(connection_socket, "ERROR: Unknown command")
                    print(f"ERROR: Unknown command '{cmd}'")
                    continue

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Client disconnected")
            connection_socket.close()


if __name__ == "__main__":
    main()
