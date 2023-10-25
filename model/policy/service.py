from ..types import StateType, ParamType
from ..spaces import (
    service_join_space,
    service_entity_space,
    service_linking_space,
    service_leave_space,
    service_linking_space,
)
from typing import Tuple, List
from ..classes import Service


def service_join_policy(
    state: StateType, params: ParamType, domain: Tuple[service_join_space]
) -> Tuple[service_entity_space]:
    space: service_join_space = domain[0]
    # Create entity
    service = Service(
        name=space["name"],
        portal_api_prefix=space["portal_api_prefix"],
        service_id=space["service_id"],
        servicers=[],
    )
    return ({"service": service},)


def service_linking_policy(
    state: StateType, params: ParamType, domain: Tuple[service_linking_space]
) -> Tuple[service_linking_space]:
    # Auto pass through
    return domain


def service_leave_policy(
    state: StateType, params: ParamType, domain: Tuple[service_leave_space]
) -> Tuple[List[service_linking_space], List[service_entity_space]]:
    spaces1 = []
    spaces2 = []
    services = domain[0]["services"]
    for service in services:
        if services[service]:
            for servicer in service.servicers:
                spaces1.append({"service": service, "servicer": servicer})
            spaces2.append({"service": service})
    return (spaces1, spaces2)
