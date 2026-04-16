This is the codebase for CPSC 471 FTP Server project

Developed and tested on Python 3.14.2

## To run:

1. Clone the repo

2. Create a virtual environment inside:
`python3 -m venv venv`

3. Activate it:
- macOS/Linux: `source venv/bin/activate`

3. Install the dependencies:
`pip install -r requirements.txt`

4. Run:
- server: `python serv.py <port number>`
- client: `python cli.py <server ip> <port number>`