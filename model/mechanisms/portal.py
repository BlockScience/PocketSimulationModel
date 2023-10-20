from ..types import StateType, ParamType
from ..spaces import portal_join_space, portal_entity_space
from typing import Tuple


def add_portal(
    state: StateType, params: ParamType, domain: Tuple[portal_entity_space]
) -> None:
    space: portal_entity_space = domain[0]
    state["Portals"].append(space["Portal"])
