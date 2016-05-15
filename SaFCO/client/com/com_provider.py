#!/usr/bin/python3
import serial
from com import constants
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
    raise RuntimeError("Device is not plugged in")
         
            
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
    if response == constants.fatal_error:
        raise RuntimeError("Command not supported")
    elif response == constants.power_supply_error:
        raise RuntimeError("Power supply error") 


#response example b"res: 1\n", b"res: 0\n", b"res: 200, 230\n"
def parse_response(response, is_bool_response=True):
    cut_response = response.replace(b"\n", b"")
    cut_response = cut_response.replace(b"\r", b"")
    check_for_fatal_errors(cut_response)
    
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

def write_command(port, command):
    port.flushInput()
    port.write(command)
    port.flush()
    

def wait_response(port, is_bool_response=True):
    while(True):
        response = port.readline()
            
        if len(response) > 0:
            port.flushOutput()
            return parse_response(response, is_bool_response)
    

def move_drill(x, y):
    port = get_port()
    move_command = get_command(constants.move_command, [x, y])
    write_command(port, move_command)
    return wait_response(port)


def drill_circuit(x, y):
    x = int(x)
    y = int(y)
    port = get_port()
    drill_command = get_command(constants.drill_command, [x, y])
    write_command(port, drill_command)
    return wait_response(port)
            

def touch_circuit():
    port = get_port()
    touch_command = get_command(constants.touch_command)
    write_command(port, touch_command)
    return wait_response(port)


def get_drill_coordinates():
    port = get_port()
    coordinates_command = get_command(constants.coordinates_command)
    write_command(port, coordinates_command)
    return wait_response(port, False)

if __name__ == "__main__":
    pass
    #open_driller_port()
        
    #print(touch_circuit())
    #print(move_drill(0, 900))
    #print(drill_circuit(0, 1000))
    #print(get_drill_coordinates())
    #print(touch_circuit())
    
    #close_driller_port()