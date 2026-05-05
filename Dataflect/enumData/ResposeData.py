from enum import Enum

class ResposeData(Enum):
    Error = ("Empty text",404)
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"