from ..types import StateType, ParamType, SessionType, ApplicationEntityType
from ..spaces import (
    application_join_space,
    application_entity_space,
    application_delegate_to_gateway_space,
    submit_relay_request_space,
    new_session_space,
    application_leave_space,
    application_undelegation_space,
)
from typing import Tuple, Union, Dict
from ..classes import Application
import random


def application_join_policy(
    state: StateType, params: ParamType, domain: Tuple[application_join_space]
) -> Tuple[Union[application_entity_space, None]]:
    space: application_join_space = domain[0]

    if space["stake_amount"] < params["minimum_application_stake"]:
        return (None,)

    # Create entity
    application = Application(
        name=space["name"],
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
        services=[],
        geo_zone=space["geo_zone"],
        number_of_services=space["number_servicers"],
        stake_status="Staked",
        unstaking_height=None,
        delegate=None,
    )
    return ({"application": application},)


def gateway_delegation_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_gateway_space],
) -> Tuple[
    Union[application_delegate_to_gateway_space, None],
    Union[application_delegate_to_gateway_space, None],
]:
    space: application_delegate_to_gateway_space = domain[0]
    # Pass through

    return (space, space)


def submit_relay_requests_policy(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> Tuple[new_session_space, new_session_space]:
    if params["submit_relay_requests_policy_function"] == "test":
        return submit_relay_requests_policy_test(state, params, domain)
    else:
        assert False, "Invalid submit_relay_requests_function"


def submit_relay_requests_policy_test(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> Tuple[new_session_space, new_session_space]:
    num_servicers = domain[0]["application_address"].number_of_services
    servicers = random.sample(state["Servicers"], num_servicers)
    service = random.choice(state["Services"])
    session: SessionType = {
        "application": domain[0]["application_address"],
        "fishermen": None,
        "geo_zone": domain[0]["application_address"].geo_zone,
        "id": None,
        "num_session_blocks": None,
        "service": service,
        "servicers": servicers,
        "session_height": None,
        "session_number": None,
    }
    return ({"session": session}, {"session": session})


def application_leave_policy(
    state: StateType, params: ParamType, domain: Tuple[application_leave_space]
) -> Tuple[
    Dict[ApplicationEntityType, Union[application_undelegation_space, None]],
    application_leave_space,
]:
    applications = domain[0]["applications"]
    space1: Dict[
        ApplicationEntityType, Union[application_undelegation_space, None]
    ] = {}
    space2 = domain[0]
    for application in applications:
        if applications[application]:
            if application.delegate:
                space1[application] = {
                    "application_public_key": application,
                    "gateway_public_key": application.delegate,
                }
            else:
                space1[application] = None
        else:
            space1[application] = None

    space2 = domain[0]

    return (space1, space2)


def gateway_undelegation_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_undelegation_space],
) -> Tuple[Union[application_undelegation_space, None],]:
    # Pass through

    return domain
