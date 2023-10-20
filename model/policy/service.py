from ..types import StateType, ParamType
from ..spaces import service_join_space, service_entity_space, service_linking_space
from typing import Tuple
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
    )
    return ({"service": service},)


def service_linking_policy(state: StateType, params: ParamType, domain: Tuple[service_linking_space]
) -> Tuple[service_linking_space]:
    return (None,)