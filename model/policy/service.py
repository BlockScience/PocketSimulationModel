from ..types import StateType, ParamType
from ..spaces import service_join_space, service_entity_space
from typing import Tuple
from ..classes import service


def service_join_policy(
    state: StateType, params: ParamType, domain: Tuple[service_join_space]
) -> Tuple[service_entity_space]:
    space: service_join_space = domain[0]
    # Create entity
    service = service(
        name=space["name"],
        portal_api_prefix=space["portal_api_prefix"],
        service_id=space["service_id"],
    )
    return ({"service": service},)