from protocol import Server
from readerwriterlock import rwlock
from database import Database
import threading
import sys

def message_break_drown(message):
    content = None
    splited_message = message.split("\n")
    line = splited_message.pop(0)
    if len(splited_message) >= 3:
        content = splited_message.pop()
    parameters = splited_message
    return (line, parameters, content)


def response_parameterizer(action, db_output = None, key = None):
    response_parameters = []
    if action == "connect":
        response_parameters.append("IP_Server:ubuntu")
        response_parameters.append("port:50007")
    elif action == "disconnect":
        response_parameters = []
    elif action == "insert":
        response_parameters.append("key:"+str(db_output))
    elif action == "get":
        response_parameters.append("type:text")
        response_parameters.append("size:"+str(sys.getsizeof(db_output)))
    elif action == "update":
        response_parameters = []
    elif action == "delete":
        if "Error" in db_output:
            response_parameters.append("key:"+str(key))
    elif action == "peek":
        response_parameters.append("existing_key:"+str(db_output))
    elif action == "list":
        response_parameters.append("type:text")
        response_parameters.append("type:"+str(sys.getsizeof(db_output)))
    response_parameters = "\n".join(response_parameters)
    return response_parameters


def db_handler(database, action, key=None, value=None):
    db_output = None
    if action == "insert":
        db_output = database.insert(value, key)
    elif action == "get":
        db_output = database.get(key)
    elif action == "peek":
        db_output = database.peek(key)
    elif action == "update":
        db_output = database.update(key,value)
    elif action == "delete":
        db_output = database.delete(key)
    elif action == "list":
        db_output = database.list()
    return db_output


def request_handler(client_socket, request, database):
    version = "ver1.0"
    db_output, action, key, value = None, None, None, None
    response_line, response_parameters, response_content = "", [], None
    (request_line, request_parameters, request_content) = message_break_drown(request)
    action = request_line.split(" ")[0]
    for p in request_parameters:
        if "key" in p:
            key = int(p.split(":")[1])
            break
    value = request_content
    if action in ["insert","get","update","delete","peek","list"]:
        db_output = db_handler(database, action, key, value)
        if action in ["get","list"]:
            response_content = db_output
    response_parameters = response_parameterizer(action, db_output, key)
    if action == "insert":
        if "Error" not in str(response_parameters):
            response_line = "003" +" "+version
        else:
            response_line = "103" +" "+version
    elif action == "update":
        if database.peek(key):
            response_line = "004" +" "+version
        else:
            response_line = "105" +" "+version
    elif action == "delete":
        if database.peek(key):
            response_line = "005" +" "+version
        else:
            response_line = "108" +" "+version
    elif action == "connect":
        if "Error" not in str(response_parameters):
            response_line = "001" +" "+version
        else:
            response_line = "101" +" "+version
    elif action == "disconnect":
        if "Error" not in str(response_parameters):
            response_line = "002" +" "+version
        else:
            response_line = "203" +" "+version
    else:
        response_line = "000" +" "+version
    print("response is sent...")
    server.send_response(client_socket, response_line, response_parameters, response_content)


def client_handler(server, client_socket, database):
    print("one client is connected...")
    while True:
        request = server.receive_request(client_socket)
        request_handler(client_socket, request, database)


def connections_handler(server, database):
    while True:
        client_socket = server.accept_client_socket()
        args = (server, client_socket, database)
        client_thread = threading.Thread(target=client_handler, args=args)
        client_thread.start()


if __name__ == "__main__":
    database = Database()
    server = Server()
    server.run_server_socket("ubuntu" ,50007 ,5)
    connections_handler(server, database)
