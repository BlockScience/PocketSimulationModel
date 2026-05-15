from ..types import StateType, ParamType
from ..spaces import (
    servicer_entity_space,
    modify_servicer_pokt_space,
    servicer_pause_space2,
)
from typing import Tuple


def add_servicer(
    state: StateType, params: ParamType, domain: Tuple[servicer_entity_space]
) -> None:
    space: servicer_entity_space = domain[0]
    state["Servicers"].append(space["servicer"])


def modify_servicer_pokt_holdings(
    state: StateType, params: ParamType, domain: Tuple[modify_servicer_pokt_space]
) -> None:
    domain[0]["public_key"].pokt_holdings += domain[0]["amount"]


def remove_servicer(
    state: StateType, params: ParamType, domain: Tuple[servicer_entity_space]
) -> None:
    space: servicer_entity_space = domain[0]
    state["Servicers"].remove(space["servicer"])


def modify_servicer_stake(
    state: StateType, params: ParamType, domain: Tuple[modify_servicer_pokt_space]
) -> None:
    domain[0]["public_key"].staked_pokt += domain[0]["amount"]
    domain[0]["public_key"].staked_pokt_total_inflow += domain[0]["amount"]


def servicer_update_pause_height(
    state: StateType, params: ParamType, domain: Tuple[servicer_pause_space2]
) -> None:
    domain[0]["address"].pause_height = domain[0]["height"]
