from ..types import StateType, ParamType
from ..spaces import service_join_space, service_entity_space
from typing import Tuple


def add_service(
    state: StateType, params: ParamType, domain: Tuple[service_entity_space]
) -> None:
    space: service_entity_space = domain[0]
    state["Services"].append(space["Service"])
