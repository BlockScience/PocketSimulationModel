from ..types import StateType, ParamType
from ..spaces import gateway_join_space, gateway_leave_space
from typing import Union, Tuple
import random


def gateway_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[gateway_join_space, None]]:
    if params["gateway_join_function"] == "simple_unfiform":
        return gateway_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid gateway_join_function"


def gateway_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[gateway_join_space, None]]:
    # Threshold is set by number of gateways divided by the max gateways
    threshold = len(state["Gateways"]) / params["gateway_max_number"]
    if random.random() > threshold:
        return (
            {
                "name": "",
                "stake_amount": 150000,  # The amount of uPOKT in escrow (i.e. a security deposit)
                "personal_holdings": 100,  # Unstaked POKT the gateway personally holds
            },
        )
    else:
        return (None,)


def gateway_leave_ba(state: StateType, params: ParamType) -> Tuple[gateway_leave_space]:
    if params["gateway_leave_function"] == "basic":
        return gateway_leave_ba_basic(state, params)
    else:
        assert False, "Invalid gateway_leave_function"


def gateway_leave_ba_basic(
    state: StateType, params: ParamType
) -> Tuple[gateway_leave_space]:
    leaves = {}
    for gateway in state["Gateways"]:
        leaves[gateway] = random.random() < params["gateway_leave_probability"]
    return ({"gateways": leaves},)
