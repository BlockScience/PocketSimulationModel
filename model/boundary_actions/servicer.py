from ..types import StateType, ParamType
from ..spaces import servicer_join_space
from typing import Union, Tuple
import random


def servicer_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[servicer_join_space, None]]:
    if params["servicer_join_function"] == "simple_unfiform":
        return servicer_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid servicer_join_function"


def servicer_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[servicer_join_space, None]]:
    # Threshold is set by number of applicatons divided by the max servicers
    threshold = len(state["Servicers"]) / params["servicer_max_number"]
    if random.random() > threshold:
        return (
            {
                "name": "",
                "stake_amount": 100,  # The amount of uPOKT in escrow (i.e. a security deposit)
                "geo_zone": "ABC",  # The physical geo-location identifier this Servicer registered in
                "number_servicers": 1,  # The number of Servicers requested per session
                "personal_holdings": 100,  # Unstaked POKT the servicer personally holds
                "service_url": None,
                "operator_public_key": None
            },
        )
    else:
        return (None,)
