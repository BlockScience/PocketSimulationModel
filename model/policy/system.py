from ..types import StateType, ParamType
from ..spaces import (
    distribute_fees_space,
    decrease_relay_fees_space,
    modify_validator_pokt_space,
    modify_dao_pokt_space,
)
from typing import Tuple, List
from math import isclose


def fee_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[distribute_fees_space]
) -> Tuple[
    decrease_relay_fees_space, List[modify_validator_pokt_space], modify_dao_pokt_space
]:
    accumulated_fees = state["relay_fees"]
    validator_share = accumulated_fees * params["validator_fee_percentage"]
    dao_share = accumulated_fees * params["dao_fee_percentage"]
    assert isclose(accumulated_fees, validator_share + dao_share)

    space1: decrease_relay_fees_space = {"POKT Amount": accumulated_fees}
    space2: List[modify_validator_pokt_space] = [
        ({"public_key": state["Validators"][0], "amount": validator_share},)
    ]
    space3: modify_dao_pokt_space = {"amount": dao_share}

    return (space1, space2, space3)
