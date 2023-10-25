from ..types import StateType, ParamType
from typing import Tuple
from ..spaces import modify_validator_pokt_space


def modify_validator_pokt_holdings(
    state: StateType, params: ParamType, domain: Tuple[modify_validator_pokt_space]
) -> None:
    domain[0]["public_key"].pokt_holdings += domain[0]["amount"]
