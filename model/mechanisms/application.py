from ..types import StateType, ParamType
from ..spaces import application_join_space, application_entity_space
from typing import Tuple
from ..classes import Application


def add_application(
    state: StateType, params: ParamType, domain: Tuple[application_entity_space]
) -> None:
    space: application_entity_space = domain[0]
    state["Applications"].append(space["application"])
