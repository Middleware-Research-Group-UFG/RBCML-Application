import csv
import random
import json

from .database import db
from .capability import ChannelCapability, RoleCapability

class RBCMLModel:
    def __init__(self, model: dict) -> None:
        self.roles = model['roles']
        self.connections = model['connections']

    def channel_capability(self, connection: str):
        channel = self.connections[connection]
        capabilities = channel[-1]

        return ChannelCapability(capabilities[0], capabilities[1], capabilities[2], capabilities[3])

    def get_role_capabilities(roleName):
        with open('roles.csv', 'r') as roles:
            reader = csv.reader(roles, delimiter=';')

            capabilitiesString = ""
            for data in reader:
                if data[0] == roleName:
                    capabilitiesString = data[1][1:-1]
                    break
            capabilitiesString = capabilitiesString.split(", ")
            capabilities = tuple(cap == 'True' for cap in capabilitiesString) + (False, False)
            return capabilities

    def role_capability(self, role: str, connection: str):
        connection_roles = connection.split('-')
        capabilities_list = self.connections[connection]
        
        try:
            role_index = connection_roles.index(role)
        except ValueError:
            raise ValueError(f"Role '{role}' not found in connection '{connection}'")
        
        cap = capabilities_list[role_index]
        return RoleCapability(cap[0], cap[1], cap[2], cap[3], cap[4], cap[5], cap[6], cap[7])
    
    def get_connections(self, role: str) -> list[str]:
            return list(self.connections.keys())

    @staticmethod
    def get_role_names(self):
        return list(self.roles)

    @staticmethod
    def role_exists(name):
        with open('roles.csv', 'a+') as roles:
            roles.seek(0)
            reader = csv.reader(roles, delimiter=';')
            for data in reader:
                if data[0] == name:
                    return True
            return False

    @staticmethod
    def set_role(name, capability):
        if not RBCMLModel.role_exists(name):
            with open('roles.csv', 'a') as roles:
                roles.write(f'{name};{capability}\n')
                return True
        else:
            return False


def get_model(session: str) -> RBCMLModel:
    session_data = db.search(session, "SessionID", "Sessions")[0]
    if session_data:
        model_id = session_data['ModelId']
        print(f"Loading model with ID: {model_id}")
        model_data = db.search(model_id, "Id", "Model")

        model_definition = json.loads(model_data['Definition'])
    return RBCMLModel("model_definition")