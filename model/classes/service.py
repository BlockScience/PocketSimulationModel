from typing import List
from ..types import ServicerEntityType

class Service:
    id_number = 0
    def __init__(self, name: str, portal_api_prefix: str, service_id: str, servicers: List[ServicerEntityType]):
        self.id_number = Service.id_number
        Service.id_number += 1
        self.name = name
        self.portal_api_prefix = portal_api_prefix
        self.service_id = service_id
        self.servicers = []