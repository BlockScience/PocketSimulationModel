from ..types import StateType, ParamType
from ..spaces import (
    portal_entity_space,
    application_delegate_to_portal_space,
    modify_portal_pokt_space,
    application_undelegation_space,
)
from typing import Tuple


def add_portal(
    state: StateType, params: ParamType, domain: Tuple[portal_entity_space]
) -> None:
    space: portal_entity_space = domain[0]
    state["Portals"].append(space["portal"])


def add_portal_delegator(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_portal_space],
) -> None:
    space: application_delegate_to_portal_space = domain[0]
    space["portal_public_key"].delegators.append(space["application_public_key"])


def modify_portal_stake(
    state: StateType, params: ParamType, domain: Tuple[modify_portal_pokt_space]
) -> None:
    domain[0]["public_key"].staked_pokt += domain[0]["amount"]


def remove_portal_delegator(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_undelegation_space],
) -> None:
    space: application_undelegation_space = domain[0]
    space["portal_public_key"].delegators.remove(space["application_public_key"])


def remove_portal(
    state: StateType,
    params: ParamType,
    domain,
) -> None:
    space = domain[0]
    state["Portals"].remove(space["portal"])
