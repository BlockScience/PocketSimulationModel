from ..types import StateType, ParamType, SessionType
from ..spaces import (
    application_entity_space,
    application_delegate_to_portal_space,
    submit_relay_request_space,
    modify_application_pokt_space,
    servicer_relay_space,
)
from typing import Tuple


def add_application(
    state: StateType, params: ParamType, domain: Tuple[application_entity_space]
) -> None:
    space: application_entity_space = domain[0]
    state["Applications"].append(space["application"])


def update_application_delegate(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_portal_space],
) -> None:
    space: application_delegate_to_portal_space = domain[0]
    space["application_public_key"].delegate = space["portal_public_key"]


def create_new_session(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> None:
    state["Sessions"].append(domain[0]["session"])


def modify_application_stake(
    state: StateType, params: ParamType, domain: Tuple[modify_application_pokt_space]
) -> None:
    domain[0]["public_key"].staked_pokt += domain[0]["amount"]


def remove_session(
    state: StateType, params: ParamType, domain: Tuple[servicer_relay_space]
) -> None:
    state["Sessions"].remove(domain[0]["session"])
