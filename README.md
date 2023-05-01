# Zandronum Server Launcher

This is a simple server launcher web application for Zandronum, a multiplayer source port for the classic first-person shooter, Doom. The application is built using Python Flask, and allows users to launch ~~and manage~~ multiple Zandronum servers from a web interface.

This is a personal project intended to be executed on a Synology for **fun only**.

A lot of problems will never be solved.

**No security aspects have been considered.**

**Use at your own risk !!!**

## Features

- Launch multiple Zandronum servers simultaneously
- Support for custom mods and WAD files
- Configurable server settings
- Server launch rate limiting per IP address (it works behind a reverse proxy)

## Known issue

- Zandronum servers never stop. The log scan and last connection detection function does not work.
- This code does not use a WSGI server. It should not be used as is on a server open to the web.
- `cmd.extend(['-servername', '"', servername, '"'])` add space in the server name.
- The management of the servers from the web page is not implemented. It should be possible with the detection of the IP address to manage its own server.
- It is not possible to run zandronum-server from the binary in /zanbin. There is a big unresolved dependency problem. It is better to use the installation method explained on the zandronum website ([https://zandronum.com/download#instubuntu](https://zandronum.com/download#instubuntu))

## Getting Started

### Prerequisites

- Python 3
- ~~Zandronum server executable~~

## Installation

### Installation without docker

1. Clone the repository or download the source code.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Set the path to your Zandronum server executable in the `zandronum_server_path` variable in the `app.py` file.
4. (Optional) Set the range of ports that the server can use by changing the values of the `next_available_port` and `last_available_port` variables in the `app.py` file.
5. (Optional) Configure the application settings in the `config.py` file.
6. (Optional) Use the screen command to run in the background

#### Usage

1. Start the server by running `python app.py`.
2. Open a web browser and go to `http://localhost:6556/`.
3. Configure the server settings and click the "Launch Server" button.
4. Wait for the server to start, and then click the "Connect" button to join the server.

### Installation without docker

```console
$ docker-compose build
$ docker-compose up -d
```
