from ..types import StateType, ParamType
from ..spaces import application_join_space, application_entity_space, application_delegate_to_portal_space
from typing import Tuple, Union
from ..classes import Application


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
    state: StateType, params: ParamType, domain: Tuple[application_delegate_to_portal_space]
) -> Tuple[Union[application_delegate_to_portal_space, None], Union[application_delegate_to_portal_space, None]]:
    space: application_delegate_to_portal_space = domain[0]
    # Pass through

    return (space, space)