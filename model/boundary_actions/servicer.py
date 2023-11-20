from ..types import StateType, ParamType, ServiceEntityType
from ..spaces import (
    servicer_join_space,
    service_linking_space,
    servicer_relay_space,
    servicer_leave_space,
    service_unlinking_space,
    servicer_stake_space,
    jail_node_space,
    unjail_node_space,
)
from typing import Union, Tuple, List
import random
import numpy as np


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
                "stake_amount": params[
                    "minimum_stake_servicer"
                ],  # The amount of uPOKT in escrow (i.e. a security deposit)
                "geo_zone": random.choice(
                    state["Geozones"]
                ),  # The physical geo-location identifier this Servicer registered in
                "personal_holdings": max(
                    np.random.normal(30937797160586.477, 25104455260369.2),
                    30000000000000 * 0.05,
                ),  # Unstaked POKT the servicer personally holds
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


def servicer_leave_ba(
    state: StateType, params: ParamType
) -> Tuple[servicer_leave_space]:
    if params["servicer_leave_function"] == "basic":
        return servicer_leave_ba_basic(state, params)
    else:
        assert False, "Invalid servicer_leave_function"


def servicer_leave_ba_basic(
    state: StateType, params: ParamType
) -> Tuple[servicer_leave_space]:
    leaves = {}
    for servicer in state["Servicers"]:
        leaves[servicer] = random.random() < params["servicer_leave_probability"]
    return ({"servicers": leaves},)


def service_unlinking_ba(
    state: StateType, params: ParamType, servicer: ServiceEntityType
) -> List[Tuple[service_unlinking_space]]:
    if params["service_unlinking_function"] == "basic":
        return service_unlinking_ba_basic(state, params, servicer)
    else:
        assert False, "Invalid service_unlinking_function"


def service_unlinking_ba_basic(
    state: StateType, params: ParamType, servicer: ServiceEntityType
) -> List[Tuple[service_unlinking_space]]:
    # Simple test function where if maximum services is not reached then the current options are joined in reverse order
    out = []
    for service in servicer.services:
        if random.random() < params["service_unlinking_probability"]:
            out.append(({"service": service, "servicer": servicer},))
    return out


def servicer_stake_ba(
    state: StateType, params: ParamType
) -> List[Tuple[servicer_stake_space]]:
    if params["servicer_stake_function"] == "basic":
        return servicer_stake_ba_basic(state, params)
    else:
        assert False, "Invalid servicer_stake_function"


def servicer_stake_ba_basic(
    state: StateType, params: ParamType
) -> List[Tuple[servicer_stake_space]]:
    out = []
    for servicer in state["Servicers"]:
        if servicer.staked_pokt < params["minimum_stake_servicer"]:
            amount = min(
                servicer.pokt_holdings,
                params["minimum_stake_servicer"] - servicer.staked_pokt,
            )
            space: servicer_stake_space = {
                "geo_zone": servicer.geo_zone,
                "operator_public_key": servicer.operator_public_key,
                "public_key": servicer,
                "service_url": servicer.service_url,
                "services": servicer.services,
                "stake_amount": amount,
            }
            out.append((space,))
    return out


def jailing_ba(state: StateType, params: ParamType) -> List[Tuple[jail_node_space]]:
    if params["jailing_function"] == "basic":
        return jailing_ba_basic(state, params)
    else:
        assert False, "Invalid jailing_function"


def jailing_ba_basic(
    state: StateType, params: ParamType
) -> List[Tuple[jail_node_space]]:
    out = []
    for servicer in state["Servicers"]:
        if servicer.pause_height:
            continue
        if random.random() < params["servicer_jailing_probability"]:
            space = (
                {
                    "block_height": state["height"],
                    "jailer_address": None,
                    "node_address": servicer,
                },
            )
            out.append(space)
    return out


def unjailing_ba(state: StateType, params: ParamType) -> List[Tuple[unjail_node_space]]:
    out: List[Tuple[unjail_node_space]] = []
    for servicer in state["Servicers"]:
        if servicer.pause_height:
            out.append(({"block_height": state["height"], "node_address": servicer},))
    return out
