import json
import socket

def message_formater(line, parameters, content=None):
    params = "\n".join([str(p) for p in parameters])
    message = f"{line}\n{parameters}"
    if content != None:
        message += f"\n{content}"
    return message


# message encoder:
# se encarga de recibir componentes del mensaje y retornarlo en un formato para el socket
def message_encoder(message):
    return message.encode()

# message decoder:
# se encarga de recibir un mensaje del socket y retornarlo en el formato original
def message_decoder(encoded_message):
    return encoded_message.decode()

class Server():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # connect server socket
    def run_server_socket(self, hostname ,port ,maxclients):
        self.socket.bind((hostname, port))
        self.socket.listen(maxclients)

    # connect client socket
    def accept_client_socket(self):
        print("server is waiting clients...")
        (clientsocket, address) = self.socket.accept()
        return clientsocket

    # disconnect server socket
    def disconnect_server_socket(self):
        self.socket.close()


    # disconnect client socket
    def disconnect_client_socket(self,fd_client_socket):
        self.socket.close(fd_client_socket)


    # send response
    def send_response(self,client_socket, line, parameters, content):
        message = message_formater(line, parameters, content)
        encoded_message = message_encoder(message)
        client_socket.send(encoded_message)


    # receive request
    def receive_request(self, client_socket):
        encoded_message = client_socket.recv(4096)
        message = message_decoder(encoded_message)
        return message


    # status
    def get_status_data(self, type = None):
        data = {"status data":""}
        status_path = "protocol_status.json"
        with open(status_path) as json_file:
            data = json.load(json_file)
            if type in ["successful","client error","server error"]:
                data = data["status data"][type]
        return data

    def get_status_by_type_and_code(self, type, code):
        data = self.get_status_data(type)
        for status in data:
            if status["code"] == code:
                return status
        return "Error: code or type doesnt exist"

    def get_status_by_code(self, code):
        data = self.get_status_data()
        for type in ["successful","client error","server error"]:
            for status in data["status data"][type]:
                if status["code"] == code:
                    return status
        return "Error: code or type doesnt exist"

    # server exceptions handler



class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # connect client socket
    def connect(self, hostname, port):
        self.socket.connect((hostname, port))


    # disconnect client socket
    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        pass


    # send request
    def send_request(self, line, parameters, content):
        message = message_formater(line, parameters, content)
        encoded_message = message_encoder(message)
        self.socket.send(encoded_message)


    # receive response
    def receive_response(self):
        encoded_message = self.socket.recv(4096)
        message = message_decoder(encoded_message)
        return message

    def is_alive(self):
        if self.socket.fileno() == -1:
            return False
        return True


    # status
    def get_status_data(self, type = None):
        data = {"status data":""}
        status_path = "protocol_status.json"
        with open(status_path) as json_file:
            data = json.load(json_file)
            if type in ["successful","client error","server error"]:
                data = data["status data"][type]
        return data


    def get_status_by_code(self, code):
        data = self.get_status_data()
        for type in ["successful","client error","server error"]:
            for status in data["status data"][type]:
                if status["code"] == code:
                    return status
        return "Error: code or type doesnt exist"


    # client exceptions handler
    def is_connected(self):
        try:
            peername = self.socket.getpeername()
            #print(peername)
            return True
        except:
            return False
