from ..types import StateType, ParamType
from ..spaces import (
    distribute_fees_space,
    decrease_relay_fees_space,
    modify_validator_pokt_space,
    modify_dao_pokt_space,
)
from typing import Tuple, List


def fee_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[distribute_fees_space]
) -> Tuple[
    decrease_relay_fees_space, List[modify_validator_pokt_space], modify_dao_pokt_space
]:
    return (
        {},
        [
            (),
        ],
        {},
    )
