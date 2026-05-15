from typing import List
from ..types import ServicerEntityType


class Service:
    id_number = 0

    def __init__(
        self,
        name: str,
        gateway_api_prefix: str,
        service_id: str,
        servicers: List[ServicerEntityType],
        join_height: int,
    ):
        self.id_number = Service.id_number
        Service.id_number += 1
        self.name = name
        self.gateway_api_prefix = gateway_api_prefix
        self.service_id = service_id
        self.servicers = servicers
        self.join_height = join_height
        self.shutdown = False
