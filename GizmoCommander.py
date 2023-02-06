import asyncio

#IP of this base station
BASE_IP = '10.65.70.129'

# seconds between commands
COMMAND_INTERVAL = 0.5
# PORT the EEG classification program is sending to
EEG_PORT = 26783
# IP of Gizmo
GIZMO_IP = '10.65.65.87'
# Port that Gizmo's head direction program is sending to
GIZMO_PORT = 26784
# IP of this base station

# 1 byte messages (just receiving booleans)
MSG_SIZE = 1

# global variables used in logic for commanding gizmo
# These variables represent the latest boolean received from each TCP server
isJawClenched = False
isFacingGizmo = True

def isBoolean(msg):
    return msg.lower() in ['true','false','0','1','t','f']

def toBoolean(msg):
    return msg.lower() in ['true','1','t']

    
async def getMessage(reader):
    msg = await reader.read(MSG_SIZE)
    
    return msg.decode().rstrip()
    
# Read 1 byte from the TCP socket. We expect either 1 or 0 representing true or false respectively
# If the message is correctly formatted. update the corresponding global variable
async def collect_latest_jaw_clench_data(reader,writer):
    while (True):
        msg = await getMessage(reader)
        
        if msg and isBoolean(msg):
            global isJawClenched
            isJawClenched = toBoolean(msg)

# Read 1 byte from the TCP socket. We expect either 1 or 0 representing true or false respectively
# If the message is correctly formatted. update the corresponding global variable          
async def collect_latest_head_direction_data(reader,writer):
    while (True):
        msg = await getMessage(reader)
        if msg and isBoolean(msg):
            global isFacingGizmo
            isFacingGizmo = toBoolean(msg)
        
        
# Create the TCP server that will recieve messages from the EEG classification program
async def eeg_server(ipAddress):
    # For every new TCP connection to this server, a new task is created and runs the
    # input function in the start_server() call
    server = await asyncio.start_server(collect_latest_jaw_clench_data,ipAddress, EEG_PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    # this task never terminates unless explicitly told to
    async with server:
        await server.serve_forever()
    
# Create the TCP server that will recieve messages from the head direction program on Gizmo
async def gizmo_server(ipAddress):
    # For every new TCP connection to this server, a new task is created and runs the
    # input function in the start_server() call
    server = await asyncio.start_server(collect_latest_head_direction_data, ipAddress, GIZMO_PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    # this task never terminates unless explicitly told to
    async with server:
        await server.serve_forever()

# TODO create HTTP client for gizmo control HTTP server
async def determineCommand(isJawClenched, isFacingGizmo):
    # if patient sees gizmo
    if isJawClenched and isFacingGizmo:
        print()
        # move farther forward
    # else if patient is looking at gizmo but doesnt see it
    elif not isJawClenched and isFacingGizmo:
        # move backward
        print()
    # else, patient not looking at gizmo! stop gizmo until they look again
    else:
        #stop
        print()


async def direct_gizmo():
    # writer = await asyncio.open_connection(GIZMO_IP, GIZMO_PORT)
    while (True):
        await asyncio.sleep(COMMAND_INTERVAL)
        print( 'isJawClenched = ' + str(isJawClenched))
        print('isFacingGizmo = ' + str(isFacingGizmo))
        determineCommand(isJawClenched, isFacingGizmo)


async def main():
    # Initially, three tasks are created. However, for each client that connects to a server
    # another task will be generated
    async with asyncio.TaskGroup() as tg:
      eeg_server_task = tg.create_task(eeg_server(BASE_IP))
      gizmo_server_task = tg.create_task(gizmo_server(BASE_IP))
      direct_gizmo_task = tg.create_task(direct_gizmo())
      # take keyboard input tasks (to shut it down)
      

# I am using asyncio, because it allows me to create multiple tasks and run them concurrently

# The big idea is that there is a loop that contains all the tasks. When a task is ready to run
# it will be given control until it voluntarily gives up control through an "await" keyword.
# These keywords are used whenever calling a function labeled with "async"
# Tasks will not be chosen to run if they are sleeping or waiting for IO
if __name__ == '__main__':
    asyncio.run(main())