import json

class Host:

    def __init__(self):
        pass

    def get_status_data(type = None):
        data = {"status data":""}
        status_path = "protocol_status.json"
        with open(status_path) as json_file:
            data = json.load(json_file)
            if type in ["successful","client error","server error"]:
                data = data["status data"][type]
        return data


class Server(Host):
    def __init__(self,database):
        self.database = database


class Client(Host):
    def __init__(self):
        pass
