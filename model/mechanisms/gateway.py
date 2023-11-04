from ..types import StateType, ParamType
from ..spaces import (
    gateway_entity_space,
    application_delegate_to_gateway_space,
    modify_gateway_pokt_space,
    application_undelegation_space,
)
from typing import Tuple


def add_gateway(
    state: StateType, params: ParamType, domain: Tuple[gateway_entity_space]
) -> None:
    space: gateway_entity_space = domain[0]
    state["Gateways"].append(space["gateway"])


def add_gateway_delegator(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_gateway_space],
) -> None:
    space: application_delegate_to_gateway_space = domain[0]
    space["gateway_public_key"].delegators.append(space["application_public_key"])


def modify_gateway_stake(
    state: StateType, params: ParamType, domain: Tuple[modify_gateway_pokt_space]
) -> None:
    domain[0]["public_key"].staked_pokt += domain[0]["amount"]


def remove_gateway_delegator(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_undelegation_space],
) -> None:
    space: application_undelegation_space = domain[0]
    space["gateway_public_key"].delegators.remove(space["application_public_key"])


def remove_gateway(
    state: StateType,
    params: ParamType,
    domain,
) -> None:
    space = domain[0]
    state["Gateways"].remove(space["gateway"])
