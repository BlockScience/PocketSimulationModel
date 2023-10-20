from ..types import StateType, ParamType
from ..spaces import application_entity_space, application_delegate_to_portal_space
from typing import Tuple


def add_application(
    state: StateType, params: ParamType, domain: Tuple[application_entity_space]
) -> None:
    space: application_entity_space = domain[0]
    state["Applications"].append(space["application"])

def update_application_delegate(state: StateType, params: ParamType, domain: Tuple[application_delegate_to_portal_space]
) -> None:
    space: application_delegate_to_portal_space = domain[0]
    space["application_public_key"].delegate = space["portal_public_key"]