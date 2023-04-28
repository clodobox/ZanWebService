# Zandronum Server Launcher

This is a simple server launcher web application for Zandronum, a multiplayer source port for the classic first-person shooter, Doom. The application is built using Python Flask, and allows users to launch and manage multiple Zandronum servers from a web interface.

This is a personal project just for fun.
A lot of problems will never be solved.

**Use at your own risk !!!**

## Features

- Launch and manage multiple Zandronum servers simultaneously
- Support for custom mods and WAD files
- Configurable server settings
- Server status and logs displayed in real-time
- Automatic cleanup of server logs
- Server launch rate limiting per IP address
- Integrated help documentationFeatures

## Known issue

- Zandronum servers never stop. The log scan and last connection detection function does not work
- This code does not use a WSGI server. It should not be used as is on a server open to the web
- The server name cannot contain any whitespace. The command is not between quotation marks.

## Getting Started

### Prerequisites

- Python 3
- Zandronum server executable

## Installation
### Installation without docker

1. Clone the repository or download the source code.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Set the path to your Zandronum server executable in the `zandronum_server_path` variable in the `app.py` file.
4. (Optional) Set the range of ports that the server can use by changing the values of the `next_available_port` and `last_available_port` variables in the `app.py` file.
5. (Optional) Configure the application settings in the `config.py` file.
6. (Optional) Use the screen command to run in the background

### Installation with docker

```console
$ docker-compose build
$ docker-compose up -d
```

### Usage

1. Start the server by running `python app.py`.
2. Open a web browser and go to `http://localhost:5000/`.
3. Configure the server settings and click the "Launch Server" button.
4. Wait for the server to start, and then click the "Connect" button to join the server.
