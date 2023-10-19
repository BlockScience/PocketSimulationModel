from ..types import StateType, ParamType
from ..spaces import application_join_space
from typing import Union, Tuple
import random


def application_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[application_join_space, None]]:
    if params["application_join_function"] == "simple_unfiform":
        return application_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid application_join_function"


def application_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[application_join_space, None]]:
    # Threshold is set by number of applicatons divided by the max applications
    threshold = len(state["Applications"]) / params["application_max_number"]
    if random.random() > threshold:
        return (
            {
                "name": "",
                "stake_amount": 100,  # The amount of uPOKT in escrow (i.e. a security deposit)
                "geo_zone": "ABC",  # The physical geo-location identifier this Servicer registered in
                "number_servicers": 1,  # The number of Servicers requested per session
                "personal_holdings": 100,  # Unstaked POKT the application personally holds
            },
        )
    else:
        return (None,)
