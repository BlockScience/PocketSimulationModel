from ..types import StateType, ParamType, ServiceEntityType
from ..spaces import (
    servicer_join_space,
    service_linking_space,
    servicer_relay_space,
    servicer_leave_space,
)
from typing import Union, Tuple, List
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
                "operator_public_key": None,
            },
        )
    else:
        return (None,)


def service_linking_ba(
    state: StateType, params: ParamType, servicer: ServiceEntityType
) -> List[Tuple[service_linking_space]]:
    if params["service_linking_function"] == "test":
        return service_linking_test(state, params, servicer)
    else:
        assert False, "Invalid service_linking_function"


def service_linking_test(
    state: StateType, params: ParamType, servicer: ServiceEntityType
) -> List[Tuple[service_linking_space]]:
    # Simple test function where if maximum services is not reached then the current options are joined in reverse order
    if len(servicer.services) == params["service_max_number_link"]:
        return []
    else:
        out = []
        ct = params["service_max_number_link"] - len(servicer.services)
        for service in state["Services"][::-1]:
            if service not in servicer.services:
                out.append(({"service": service, "servicer": servicer},))
                ct -= 1
                if ct == 0:
                    break
        return out


def relay_requests_ba(
    state: StateType, params: ParamType
) -> Tuple[servicer_relay_space]:
    if params["relay_requests_function"] == "test":
        return relay_requests_ba_test(state, params)
    else:
        assert False, "Invalid relay_requests_function"


def relay_requests_ba_test(
    state: StateType, params: ParamType
) -> Tuple[servicer_relay_space]:
    session = state["Sessions"][0]
    out: servicer_relay_space = {
        "applications": session["application"],
        "servicers": session["servicers"],
        "session": session,
    }
    return (out,)


def servicer_leave_ba(state: StateType, params: ParamType) -> servicer_leave_space:
    pass
