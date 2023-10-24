from ..types import StateType, ParamType, SessionType
from ..spaces import (
    application_join_space,
    application_entity_space,
    application_delegate_to_portal_space,
    submit_relay_request_space,
    new_session_space,
    application_leave_space,
)
from typing import Tuple, Union
from ..classes import Application
import random


def application_join_policy(
    state: StateType, params: ParamType, domain: Tuple[application_join_space]
) -> Tuple[application_entity_space]:
    space: application_join_space = domain[0]
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


def portal_delegation_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_portal_space],
) -> Tuple[
    Union[application_delegate_to_portal_space, None],
    Union[application_delegate_to_portal_space, None],
]:
    space: application_delegate_to_portal_space = domain[0]
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
) -> Tuple[application_leave_space]:
    pass
