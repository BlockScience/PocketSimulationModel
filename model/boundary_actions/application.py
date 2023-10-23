from ..types import StateType, ParamType, ApplicationEntityType
from ..spaces import (
    application_join_space,
    application_delegate_to_portal_space,
    submit_relay_request_space,
)
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


def portal_delegation_ba(
    state: StateType, params: ParamType, application: ApplicationEntityType
) -> Tuple[Union[application_delegate_to_portal_space, None]]:
    if params["portal_delegation_function"] == "test":
        return portal_delegation_ba_test(state, params, application)
    else:
        assert False, "Invalid portal_delegation_function"


def portal_delegation_ba_test(
    state: StateType, params: ParamType, application: ApplicationEntityType
) -> Tuple[Union[application_delegate_to_portal_space, None]]:
    if (
        not application.delegate
        and application.id_number % 2 == 1
        and len(state["Portals"]) > 0
    ):
        portal = random.choice(state["Portals"])
        return ({"application_public_key": application, "portal_public_key": portal},)
    else:
        return (None,)


def submit_relay_requests_ba(
    state: StateType,
    params: ParamType,
) -> Tuple[submit_relay_request_space]:
    if params["submit_relay_requests_function"] == "test":
        return submit_relay_requests_ba_test(state, params)
    else:
        assert False, "Invalid submit_relay_requests_function"


def submit_relay_requests_ba_test(
    state: StateType,
    params: ParamType,
) -> Tuple[submit_relay_request_space]:
    application = random.choice(state["Applications"])
    return ({"application_address": application},)
