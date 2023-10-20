from ..types import StateType, ParamType
from ..spaces import service_entity_space, service_linking_space
from typing import Tuple


def add_service(
    state: StateType, params: ParamType, domain: Tuple[service_entity_space]
) -> None:
    space: service_entity_space = domain[0]
    state["Services"].append(space["service"])




def link_service_mechanism(state: StateType, params: ParamType, domain: Tuple[service_linking_space]
) -> None:
    service = domain[0]["service"]
    servicer = domain[0]["servicer"]
    service.servicers.append(servicer)
    servicer.services.append(service)