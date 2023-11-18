from ..types import StateType, ParamType
from ..spaces import distribute_fees_space
from typing import Tuple


def fee_reward_ba(state: StateType, params: ParamType) -> Tuple[distribute_fees_space]:
    return ({"current_height": state["height"]},)


def block_reward_ba(state: StateType, params: ParamType) -> Tuple[None]:
    return (None,)
