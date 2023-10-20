from ..types import StateType, ParamType
from ..spaces import servicer_join_space, servicer_entity_space
from typing import Tuple


def add_servicer(
    state: StateType, params: ParamType, domain: Tuple[servicer_entity_space]
) -> None:
    space: servicer_entity_space = domain[0]
    state["Servicers"].append(space["Servicer"])
