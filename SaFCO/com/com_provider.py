#!/usr/bin/python3
import serial
import constants
from os import listdir


port = None


def set_port(serial_port):
    global port
    port = serial_port

def get_port():
    global port
    if port != None:
        return port
    else:
        raise RuntimeError('Port is not defined')    


def close_driller_port():
    port = get_port()
    if (port != None):
        port.close()


def open_driller_port():
    directory_name = "/dev/"
    
    for port_name in [f for f in listdir(directory_name) if f.startswith('ttyACM')]:
        port_path = directory_name + port_name
        
        if connect(port_path):
            return True
        else:
            raise RuntimeError("Driller port not found")
         
            
def get_command(command_prefix, parameters=[]):
    postfix = b"\n"
    if len(parameters) > 0:
        command = command_prefix
        for parameter in parameters:
            command += b" " + str(parameter).encode("ascii")
        return command + postfix
    else:
        return command_prefix + postfix


def check_for_fatal_errors(response):
    pass 


#response example b"res: 1\n", b"res: 0\n", b"res: 200, 230\n"
def parse_response(response, is_bool_response=True):
    check_for_fatal_errors(response)
    cut_response = response.replace(b"\n", b"")
    cut_response = cut_response.replace(b"\r", b"")
    
    if is_bool_response:
        response_parts = cut_response.split(b" ")
        
        if len(response_parts) >= 2:
            return True if response_parts[1] == b"1" else False
        return False
    else:
        response_parts = cut_response.split(b" ")
        
        if len(response_parts) > 2:
            return tuple([int(part) for part in response_parts[1:]])


def wait_ready():
    port = get_port()
    
    while(True):
        response = port.readline()

        if parse_response(response):
            break
              

def connect(port_path, trying_count=3):
    connect_result = False
    connect_command = get_command(constants.connect_command)
    port = serial.Serial(port_path, constants.boud_rate, timeout=constants.timeout)
    port.xonxoff = True
    port.rtscts = True
    port.dsrdtr = True    
    
    for i in range(trying_count):
        port.write(connect_command)
        response = port.readline()
            
        if parse_response(response):
            set_port(port)
            connect_result = True
            wait_ready()
            break
    return connect_result


def move_drill(x, y):
    port = get_port()
    move_command = get_command(constants.move_command, [x, y])
    port.flushInput()
    port.write(move_command)
    port.flush()
        
    while(True):
        response = port.readline()
            
        if len(response) > 0:
            port.flushOutput()
            return parse_response(response)
                    

if __name__ == "__main__":
    open_driller_port()
        
    print(move_drill(0, 500))
    print(move_drill(500, 500))
    
    close_driller_port()