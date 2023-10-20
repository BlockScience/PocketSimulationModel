from ..types import StateType, ParamType, SessionType
from ..spaces import (
    application_entity_space,
    application_delegate_to_portal_space,
    submit_relay_request_space,
)
from typing import Tuple


def add_application(
    state: StateType, params: ParamType, domain: Tuple[application_entity_space]
) -> None:
    space: application_entity_space = domain[0]
    state["Applications"].append(space["application"])


def update_application_delegate(
    state: StateType,
    params: ParamType,
    domain: Tuple[application_delegate_to_portal_space],
) -> None:
    space: application_delegate_to_portal_space = domain[0]
    space["application_public_key"].delegate = space["portal_public_key"]


def create_new_session(
    state: StateType, params: ParamType, domain: Tuple[submit_relay_request_space]
) -> None:
    assert False
    servicers = None
    session: SessionType = {
        "application": domain[0]["application_address"],
        "fishermen": None,
        "geo_zone": domain[0]["application_address"].geo_zone,
        "id": None,
        "num_session_blocks": None,
        "service": domain[0]["application_address"].service,
        "servicers": [],
    }
