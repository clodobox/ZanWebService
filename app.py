from flask import Flask, render_template, request, redirect, url_for, app
from threading import Thread
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import subprocess
import time
import datetime
import socket
import re
import time

app = Flask(__name__)
LOGS_DIR = 'logs'
server_instances = {}
launched_servers = {}
server_creations = {}
next_available_port = int(os.environ['next_available_port'])
last_available_port = int(os.environ['last_available_port'])
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
zandronum_server_path = os.environ['zandronum_server_path']

# Set Zandronum flags
dmflags = [
    {"value": 1, "description": "Disallow health (In Deathmatch)"},
    {"value": 2, "description": "Disallow powerups (In Deathmatch)"},
    {"value": 4, "description": "Weapons stay (In Deathmatch)"},
    {"value": 8, "description": "Falling damage (ZDoom)"},
    {"value": 16, "description": "Falling damage (Hexen)"},
   #{"value": 32, "description": "(unused)"},
    {"value": 64, "description": "Stay on the same map (In Deathmatch)"},
    {"value": 128, "description": "Spawn farthest (In Deathmatch)"},
    {"value": 256, "description": "Force respawn (In Deathmatch)"},
    {"value": 512, "description": "Disallow armor (In Deathmatch)"},
    {"value": 1024, "description": "Disallow exit (In Deathmatch)"},
    {"value": 2048, "description": "Infinite ammo"},
    {"value": 4096, "description": "No monsters"},
    {"value": 8192, "description": "Monsters respawn"},
    {"value": 16384, "description": "Items respawn"},
    {"value": 32768, "description": "Fast monsters"},
    {"value": 65536, "description": "Disallow jump"},
    {"value": 131072, "description": "Allow jumping"},
    {"value": 262144, "description": "Disallow freelook"},
    {"value": 524288, "description": "Mega powerups respawn"},
    {"value": 1048576, "description": "Disallow FOV"},
    {"value": 2097152, "description": "Don't spawn multiplayer weapons (In Cooperative)"},
    {"value": 4194304, "description": "Disallow crouch"},
    {"value": 8388608, "description": "Allow crouch"},
    {"value": 16777216, "description": "Lose inventory (In Cooperative)"},
    {"value": 33554432, "description": "Lose keys (In Cooperative)"},
    {"value": 67108864, "description": "Lose weapons (In Cooperative)"},
    {"value": 134217728, "description": "Lose armor (In Cooperative)"},
    {"value": 268435456, "description": "Lose powerups (In Cooperative)"},
    {"value": 536870912, "description": "Lose ammo (In Cooperative)"},
    {"value": 1073741824, "description": "Lose half ammo (In Cooperative)"},
]
dmflags2 = [
    {"value": 2, "description": "Infinite inventory"},
    {"value": 4, "description": "Double ammo"},
    {"value": 8, "description": "Instant flag return (ST/CTF)"},
    {"value": 16, "description": "No team switching (ST/CTF)"},
    {"value": 32, "description": "Server picks teams (ST/CTF)"},
    {"value": 64, "description": "Degeneration"},
    {"value": 128, "description": "Disallow spying"},
    {"value": 256, "description": "Chasecam"},
    {"value": 512, "description": "Disallow autoaim"},
    {"value": 1024, "description": "Disallow suicide"},
    {"value": 2048, "description": "No respawn protection (In Deathmatch)"},
    {"value": 4096, "description": "Start with shotgun (In Cooperative)"},
    {"value": 8192, "description": "Spawn where died (In Cooperative)"},
    {"value": 16384, "description": "No respawning"},
    {"value": 32768, "description": "Disallow automap"},
    {"value": 65536, "description": "Disallow allies on automap"},
    {"value": 131072, "description": "Barrels respawn"},
    {"value": 262144, "description": "Kill all monsters (In Cooperative)"},
    {"value": 524288, "description": "Keep frags"},
    {"value": 1048576, "description": "Disallow crouch"},
    {"value": 2097152, "description": "Lose frag when fragged"},
    {"value": 4194304, "description": "Disallow jumping"},
    {"value": 8388608, "description": "Disallow freelook"},
    {"value": 16777216, "description": "Check ammo for weapon switch"},
    {"value": 33554432, "description": "Killing Romero kills all his spawns"},
    {"value": 67108864, "description": "Count monsters in end level sectors"}
]
compatflags= [
    {"value": 1, "description": "Find shortest textures like Doom"},
    {"value": 2, "description": "Use buggier stair building"},
    {"value": 4, "description": "Limit pain elementals to 20 lost souls"},
    {"value": 8, "description": "Don't let others hear pickups"},
    {"value": 16, "description": "Actors are infinitely tall"},
    {"value": 32, "description": "Allow silent BFG trick"},
    {"value": 64, "description": "Enable wallrunning"},
    {"value": 128, "description": "Spawn item drops on the floor"},
    {"value": 256, "description": "All special lines can block use lines"},
    {"value": 512, "description": "Disable Boom door light effect"},
    {"value": 1024, "description": "Raven's scrollers use original speed"},
    {"value": 2048, "description": "Use sector based sound target code"},
    {"value": 4096, "description": "Limit deh.MaxHealth to health bonus"},
    {"value": 8192, "description": "Trace ign. lines w. s. sec on b. sides"},
    {"value": 16384, "description": "No monster dropoff move"},
    {"value": 32768, "description": "Scrolling sectors are additve"},
    {"value": 65536, "description": "Monsters see semi-invisible players"},
    {"value": 131072, "description": "Silent instant floors"},
    {"value": 262144, "description": "Sector sounds"},
    {"value": 524288, "description": "Doom missile clip"},
    {"value": 1048576, "description": "Monster drop off"},
    {"value": 2097152, "description": "Allow any bossdeath for level special"},
    {"value": 4194304, "description": "No Minotaur floor flames in water"},
    {"value": 8388608, "description": "Original A_Mushroom speed in DEH mods"},
    {"value": 16777216, "description": "Monster movement is affected by effects"},
    {"value": 33554432, "description": "Crushed monsters can be resurrected"},
    {"value": 67108864, "description": "Friendly monsters aren't blocked"},
    {"value": 134217728, "description": "Invert sprite sorting"},
    {"value": 268435456, "description": "Use Doom code for hitscan checks"},
    {"value": 536870912, "description": "Find neighboring light like Doom"},
    {"value": 1073741824, "description": "Draw polyobjects like Hexen"},
    {"value": -2147483648, "description": "Ignore Y offsets on masked midtextures"}
]
compatflags2= [
    {"value": 1, "description": "Cannot travel straight NSEW"},
    {"value": 2, "description": "Use Doom's floor motion behavior"},
    {"value": 64, "description": "Non-blocking lines can be pushed"}
]
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

@app.route('/', methods=['GET', 'POST'])

def index():
    global next_available_port
    global server_creations

    ip = request.remote_addr

    if request.method == 'POST':
        if ip not in server_creations:
            server_creations[ip] = 0


        if server_creations[ip] < 2:  # Limit server creations to 2 per IP address
            # Your existing code to launch the server
            server_creations[ip] += 1
        else:
            # Return an error message or render a template indicating the limit has been reached
            return "You have reached the limit of 2 server creations per IP address."
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!            
        # Launch the server using the form data
        print(request.form)
        #launch_server(request.form)
        launch_server(request.form)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    mods = os.listdir('mods')
    now = datetime.datetime.now()
    for server_info in launched_servers.values():
        last_connected_timestamp = get_last_connected_timestamp(server_info['log_file'])
        if last_connected_timestamp:
            elapsed_time = (now - last_connected_timestamp).seconds
            server_info['remaining_time'] = max(0, server_info['timeout'] - elapsed_time)
        else:
            server_info['remaining_time'] = server_info['timeout']
    servers = list(launched_servers.values())
    iwad_files = list_wad_files()
    return render_template('index.html', mods=mods, servers=servers, iwad_files=iwad_files, dmflags=dmflags, dmflags2=dmflags2, compatflags=compatflags, compatflags2=compatflags2)

def list_wad_files(wad_folder='wads'):
    if not os.path.exists(wad_folder):
        return []
    wad_files = [f for f in os.listdir(wad_folder) if f.lower().endswith('.wad')]
    return sorted(wad_files)

# def get_available_port(start_port, end_port):
    # for port in range(start_port, end_port+1):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # result = sock.connect_ex(('localhost', port))
            # if result != 0:
                # return port
    # return None


def launch_server(params):
    global next_available_port
    


    cmd = [zandronum_server_path]

    # difficulty & game mods setup
    # difficulty = request.form.get('difficulty')
    # game_mode = request.form.get('game_mode') 
    # if difficulty:
        # cmd.extend(["+skill", str(difficulty)])
    # if game_mode:
        # cmd.extend (["+gamemode", str(game_mode)]),

    # Process DMFlags
    dmflags = sum(int(flag) for flag in request.form.getlist('dmflags'))
    cmd.extend(['-dmflags', str(dmflags)])

    # Process DMFlags2
    dmflags2 = sum(int(flag) for flag in request.form.getlist('dmflags2'))
    cmd.extend(['-dmflags2', str(dmflags2)])
    
    # Process CompatFlags
    compatflags = sum(int(flag) for flag in request.form.getlist('compatflags'))
    cmd.extend(['-compatflags', str(compatflags)]) 
    
    # Process CompatFlags2
    compatflags2 = sum(int(flag) for flag in request.form.getlist('compatflags2'))
    cmd.extend(['-compatflags2', str(compatflags2)]) 

    # Add the full path of the selected IWAD file
    iwad_path = os.path.join('wads', params['iwad'])
    cmd.extend(['-iwad', iwad_path])
    
    # Add the server name
    servername = request.form.get('servername')
    cmd.extend(['-servername', '"', servername, '"'])

    # Add the selected mods
    for i in range(5):
        mod_key = f'mod_{i}'
        if mod_key in params and params[mod_key]:
            mod_path = os.path.join('mods', params[mod_key])
            cmd.extend(['-file', mod_path])
    
    # Add other parameters to the command
    for key, value in params.items():
        if key != 'iwad' and value:
            cmd.append(f'-{key}')
            if value not in ['true', 'false']:
                cmd.append(value)
                
    # Remove zandronum's timestamp on log file
    cmd.append('+sv_logfilenametimestamp false')

    # Get the next available port
    server_port = next_available_port
    next_available_port += 1  # Increment the port number for the next server launch

    # Check if the next available port has reached the last available port
    if next_available_port > last_available_port:
        next_available_port = 10650  # Reset the next available port

    # Get an available port
    server_port = next_available_port
    cmd.extend(['-port', str(server_port)])
    

    # Create log file
    log_file_name = f"{server_port}_{datetime.datetime.now().strftime('%d%m%y_%H%M')}.log"
    log_file_path = os.path.join(LOGS_DIR, log_file_name)

    # Add logging command
    cmd.extend(['+logfile', log_file_path])
    
    # Wait for the log file to be created
    max_attempts = 10
    sleep_interval = 0.5  # Wait for 0.5 seconds between attempts
 
    # Print the server launch command
    command_str = " ".join(cmd)
    app.logger.info(f"Launching server with command: {command_str}")
    
    # Launch the server (whtout verbose)
    # server_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Launch the server (verbose)
    server_process = subprocess.Popen(cmd)
    
    for _ in range(max_attempts):
        if os.path.exists(log_file_path):
            break
        time.sleep(sleep_interval)
    else:
        # If the log file is still not created after the maximum number of attempts
        print(f"Error: Log file {log_file_path} not created after {max_attempts * sleep_interval} seconds.")
        return
  
    # Store server information
    server_info = {
        'port': server_port,
        'start_time': datetime.datetime.now(),
        'timeout': 3600, # 1 hour
        'log_file': log_file_name,
    }
    launched_servers[str(server_port)] = server_info



def check_server_activity():
    one_hour = 60 * 60
    while True:
        time.sleep(one_hour)  # Check every hour
        current_time = time.time()
        inactive_servers = []

        for port, server_instance in server_instances.items():
            log_file = f"logs/server_{port}.log"
            recent_activity = read_log_for_activity(log_file, one_hour)

            if not recent_activity and current_time - server_instance['last_activity'] > one_hour:
                server_instance['process'].terminate()
                inactive_servers.append(port)

        # Remove inactive servers from the server_instances dictionary
        for port in inactive_servers:
            del server_instances[port]
            
def get_last_connected_timestamp(log_file):
    last_connected_timestamp = None
    timestamp_pattern = re.compile(r'\[(\d{2}:\d{2}:\d{2})\]')
    
    if not os.path.exists(log_file):
        return last_connected_timestamp

    with open(log_file, 'r') as file:
        for line in file:
            if 'connected' in line:
                match = timestamp_pattern.search(line)
                if match:
                    last_connected_timestamp = datetime.datetime.strptime(match.group(1), '%H:%M:%S')
    return last_connected_timestamp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6556, debug=True)