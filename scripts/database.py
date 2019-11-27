from protocol import Client
from random import randint


class Database:


    def __init__(self):
        self.data = {}
        self.counter = randint(1000,10000)


    def insert(self, value, user_key=None):
        key = self.counter
        if user_key != None:
            key = user_key
        else:
            self.counter += 1
        # Error si la clave ya existe
        error_message = self.validate_errors("insert",key,value)
        if error_message != None:
            return error_message
        self.data[key] = value
        # Retorna key si es exitoso
        return key


    def get(self, key):
        error_message = self.validate_errors("get",key)
        if error_message != None:
            return error_message
        return self.data[key]


    def peek(self, key):
        keys = self.data.keys()
        if key in keys:
            return True
        return False


    def update(self, key, value):
        error_message = self.validate_errors("update",key,value)
        if error_message != None:
            return error_message
        self.data[key] = value
        return "successful update"


    def delete(self, key):
        error_message = self.validate_errors("delete",key)
        if error_message != None:
            return error_message
        del self.data[key]
        return "successful delete"


    def list(self):
        available_keys = list(self.data.keys())
        return available_keys


    def key_error(self, key):
        if not isinstance(key, int):
            return "Error: key must be integer"
        if key <= 0:
            return "Error: key must be positive"
        return None


    def value_error(self, value):
        return None


    def key_exists_error(self, key):
        if self.peek(key):
            return "Error: key already exists"
        return None


    def key_doesnt_exist_error(self, key):
        if not self.peek(key):
            return "Error: key does not exist"
        return None


    def validate_errors(self, type, key=None, value=None):
        messages = []
        if type in ["get","update","delete"]:
            messages.append(self.key_doesnt_exist_error(key))
        if type == "insert":
            messages.append(self.key_exists_error(key))
        if key != None:
            messages.append(self.key_error(key))
        if value != None:
            messages.append(self.value_error(value))
        for message in messages:
            if message != None:
                return message
        return None
