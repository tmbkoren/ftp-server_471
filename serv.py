import os
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python serv.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    ## WIP
    print(f"Starting server on port {port}...")


if __name__ == "__main__":
    main()
