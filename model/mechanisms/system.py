from ..types import StateType, ParamType
from typing import Tuple
from ..spaces import (
    increase_relay_fees_space,
    decrease_relay_fees_space,
    burn_pokt_mechanism_space,
)


def increase_relay_fees(
    state: StateType, params: ParamType, domain: Tuple[increase_relay_fees_space]
) -> None:
    state["relay_fees"] += domain[0]["POKT Amount"]


def decrease_relay_fees(
    state: StateType, params: ParamType, domain: Tuple[decrease_relay_fees_space]
) -> None:
    state["relay_fees"] -= domain[0]["POKT Amount"]


def burn_pokt_mechanism(
    state: StateType, params: ParamType, domain: Tuple[burn_pokt_mechanism_space]
) -> None:
    state["floating_supply"] -= domain[0]["burn_amount"]
