from ..types import StateType, ParamType
from typing import Tuple
from ..spaces import increase_relay_fees_space


def increase_relay_fees(
    state: StateType, params: ParamType, domain: Tuple[increase_relay_fees_space]
) -> None:
    state["relay_fees"] += domain[0]["POKT Amount"]
