from ..types import StateType, ParamType
from ..spaces import service_join_space
from typing import Union, Tuple
import random


def service_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[service_join_space, None]]:
    if params["service_join_function"] == "simple_unfiform":
        return service_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid service_join_function"


def service_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[service_join_space, None]]:
    # Threshold is set by number of applicatons divided by the max services
    threshold = len(state["Services"]) / params["service_max_number"]
    if random.random() > threshold:
        return ({"name": "ABC", "portal_api_prefix": "ABC", "service_id": "ABC"},)
    else:
        return (None,)


def service_leave_ba(state: StateType, params: ParamType) -> None:
    pass
