from protocol import Client
import threading
import socket
import time
import sys

class Exit_flag:

    def __init__(self):
        self.value = False


    def activate_exit(self):
        self.value = True


    def checkout(self):
        return self.value


def request_parameterizer(command, key = None, value = None):
    request_parameters = []
    if command == "connect":
        request_parameters.append("port:50007")
        if value == None:
            request_parameters.append("IP_client:ubuntu")
        else:
            request_parameters.append("IP_client:"+str(value))
    elif command == "disconnect":
        request_parameters = []
    elif command == "insert":
        request_parameters.append("type:text")
        request_parameters.append("size:"+str(sys.getsizeof(value)))
        if(key != None):
            request_parameters.append("key:"+str(key))
    elif command == "get":
        request_parameters.append("key:"+str(key))
    elif command == "update":
        request_parameters.append("type:text")
        request_parameters.append("size:"+str(sys.getsizeof(value)))
        request_parameters.append("key:"+str(key))
    elif command == "delete":
        request_parameters.append("key:"+str(key))
    elif command == "peek":
        request_parameters.append("key:"+str(key))
    elif command == "list":
        request_parameters = []
    request_parameters = "\n".join(request_parameters)
    return request_parameters


def exec_client_connect(key=None, value=None, client=None, exit_flag = None):
    ip = "ubuntu"
    if value != None:
        ip = value
    connection_thread = threading.Thread(target=try_connect, args=(client,ip,50007,))
    connection_thread.start()
    connection_thread.join()
    if client.is_alive():
        server_thread = threading.Thread(target=server_listener, args=(client, exit_flag))
        server_thread.start()


def exec_client_disconnect(key=None, value=None, client=None, exit_flag = None):
    output = "disconnecting..."
    client.disconnect()
    print(output)


def exec_client_quit(key=None, value=None, client=None, exit_flag = None):
    exec_client_disconnect(key, value, client, exit_flag)
    exit_flag.activate_exit()
    console_output = "closing the client..."
    print(console_output)


def exec_client_insert(key=None, value=None, client=None, exit_flag = None):
    line = "insert ver1.0"
    parameters = request_parameterizer("insert",key,value)
    content = value
    client.send_request(line, parameters, content)


def exec_client_get(key=None, value=None, client=None, exit_flag = None):
    line = "get ver1.0"
    parameters = request_parameterizer("get", key)
    content = value
    client.send_request(line, parameters, content)


def exec_client_peek(key=None, value=None, client=None, exit_flag = None):
    line = "peek ver1.0"
    parameters = request_parameterizer("peek", key)
    content = value
    client.send_request(line, parameters, content)


def exec_client_update(key=None, value=None, client=None, exit_flag = None):
    line = "update ver1.0"
    parameters = request_parameterizer("update", key, value)
    content = value
    client.send_request(line, parameters, content)


def exec_client_delete(key=None, value=None, client=None, exit_flag = None):
    line = "delete ver1.0"
    parameters = request_parameterizer("delete", key)
    content = value
    client.send_request(line, parameters, content)


def exec_client_list(key=None, value=None, client=None, exit_flag = None):
    line = "list ver1.0"
    parameters = request_parameterizer("list")
    content = value
    client.send_request(line, parameters, content)


def valid_command(command):
    if command in ["connect","disconnect","quit","insert","get","peek","update","delete","list"]:
        return True
    return False


def function_handler(command, key=None, value=None, client=None, exit_flag=None):
    commads_functions = {
        "connect" : exec_client_connect,
        "disconnect" : exec_client_disconnect,
        "quit" : exec_client_quit,
        "insert" : exec_client_insert,
        "get" : exec_client_get,
        "peek" : exec_client_peek,
        "update" : exec_client_update,
        "delete" : exec_client_delete,
        "list" : exec_client_list,
    }
    return commads_functions[command](key, value, client, exit_flag)


def valid_user_input(user_input):
    if not isinstance(user_input,str):
        return "Error: input must be string"
    elif len(user_input) == 0:
        return "Error: input cant be blank"
    elif "(" in user_input and ")" != user_input[-1]:
        return "Error: invalid input syntax"
    (command,key,value) = decode_input(user_input)
    if not valid_command(command):
        return f"Error: {command} is not a command"
    elif command in ["disconnect","quit","list"] and (key != None or value != None):
        return f"Error: {command} can not have parameters"
    elif command == "connect" and (key != None and value != None):
        return f"Error: {command} can not have twoo parameters"
    elif command in ["get","peek","delete"] and ( value != None ):
        return f"Error: {command} can not have value"
    elif command in ["get","peek","delete"] and ( key == None ):
        return f"Error: {command} must have key"
    elif command == "insert" and (value == None or (value == None and key == None)):
        return "Error: insert at least must have value"
    elif command == "update" and (value == None or key == None):
        return "Error: update must have key and value"
    try:
        if key != None and int(key) < 1:
            return "Error: key must be positive"
    except:
        return "Error: key must be integer"
    return None


def decode_input(user_input):
    command, param1, param2, key, value = None, None, None, None, None
    # tipo1: comando
    if "(" not in user_input and "," not in user_input and ")" not in user_input:
        command = user_input
    # tipo2: comando(parametro)
    elif "," not in user_input and "(" in user_input and ")" in user_input:
        chunks = user_input.split("(")
        command = chunks[0]
        param1 = chunks[1][:-1]
    # tipo3: comando(parametro1, parametro2)
    elif "," in user_input and "(" in user_input and ")" in user_input:
        chunks = user_input.split("(")
        command = chunks[0]
        params = chunks[1].split(",")
        param1 = params[0]
        param2 = params[1][:-1]
    if param1 != None and param2 != None:
        key, value = param1, param2
    elif param2 == None:
        if command in ["get","peek","delete"]:
            key = param1
        elif command in ["insert","connect"]:
            value = param1
    return (command, key, value)


def process_input(user_input, client, exit_flag):
    user_input = user_input.strip()
    user_input = user_input.lower()
    error_message = valid_user_input(user_input)
    if error_message != None:
        return error_message
    (command,key,value) = decode_input(user_input)
    output = function_handler(command, key, value, client, exit_flag)
    return output


def input_listener(client, exit_flag):
    print("client is waiting for instruction...")
    while not exit_flag.checkout():
        user_input = input()
        error_message = process_input(user_input, client, exit_flag)
        if error_message != None:
            print(error_message)
        if client.is_alive():
            print("client is waiting for response...")


def message_break_drown(message):
    content = None
    splited_message = message.split("\n")
    line = splited_message.pop(0)
    if len(splited_message) >= 3:
        content = splited_message.pop()
    parameters = splited_message[0]
    return (line, parameters, content)

def response_handler(response):
    status_message = "response not handled yet"
    extra_info = None
    (line,parameters,content) = message_break_drown(response)
    status_code = line.split(" ")[0]
    if status_code in ["003"]:
        extra_info = "key: "+"".join(parameters.split(":")[1:])
    elif status_code == "000":
        extra_info = content
        if "key" in parameters:
            extra_info = "".join(parameters.split(":")[1:])
    status_message = Client().get_status_by_code(status_code)["message"]
    print(status_message)
    if extra_info != None:
        print(extra_info)


def server_listener(client, exit_flag):
    while client.is_alive() and not exit_flag.checkout():
        try:
            response = client.receive_response()
            response_handler(response)
            print("client is waiting for instruction...")
        except:
            break



def try_connect(client, ip, port):
    seconds = 0
    status_code = "100"
    while seconds < 10 and not client.is_connected():
        try:
            client.connect(ip, port)
        except:
            print("trying to connect...")
        time.sleep(1)
        seconds += 1
    if client.is_connected():
        status_code = "001"
    status_message = Client().get_status_by_code(status_code)["message"]
    console_output = status_message
    print(console_output)


def client_handler(client, exit_flag):
    connection_thread = threading.Thread(target=try_connect, args=(client,"ubuntu",50007,))
    connection_thread.start()
    connection_thread.join()
    interface_thread = threading.Thread(target=input_listener, args=(client,exit_flag))
    server_thread = threading.Thread(target=server_listener, args=(client,exit_flag))
    interface_thread.start()
    if client.is_alive() and not exit_flag.checkout():
        server_thread.start()
        server_thread.join()
    interface_thread.join()
    status_code = "002"
    status_message = Client().get_status_by_code(status_code)["message"]
    print(status_message)


if __name__ == "__main__":
    client = Client()
    exit_flag = Exit_flag()
    client_handler(client, exit_flag)
