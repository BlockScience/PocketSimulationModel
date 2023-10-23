from ..types import StateType, ParamType
from ..spaces import portal_join_space
from typing import Union, Tuple
import random


def portal_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[portal_join_space, None]]:
    if params["portal_join_function"] == "simple_unfiform":
        return portal_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid portal_join_function"


def portal_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[portal_join_space, None]]:
    # Threshold is set by number of portals divided by the max portals
    threshold = len(state["Portals"]) / params["portal_max_number"]
    if random.random() > threshold:
        return (
            {
                "name": "",
                "stake_amount": 100,  # The amount of uPOKT in escrow (i.e. a security deposit)
                "personal_holdings": 100,  # Unstaked POKT the portal personally holds
            },
        )
    else:
        return (None,)


def portal_leave_ba(state: StateType, params: ParamType) -> None:
    pass
