import os
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python cli.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    ## WIP
    print(f"Connecting to {host}:{port}...")

if __name__ == "__main__":
    main()