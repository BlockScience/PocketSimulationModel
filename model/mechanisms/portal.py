from ..types import StateType, ParamType
from ..spaces import portal_entity_space, application_delegate_to_portal_space
from typing import Tuple


def add_portal(
    state: StateType, params: ParamType, domain: Tuple[portal_entity_space]
) -> None:
    space: portal_entity_space = domain[0]
    state["Portals"].append(space["portal"])


def add_portal_delegator(state: StateType, params: ParamType, domain: Tuple[application_delegate_to_portal_space]
) -> None:
    space: application_delegate_to_portal_space = domain[0]
    space["portal_public_key"].delegators.append(space["application_public_key"])