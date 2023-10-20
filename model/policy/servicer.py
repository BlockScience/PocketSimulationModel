from ..types import StateType, ParamType
from ..spaces import (
    servicer_join_space,
    servicer_entity_space,
    servicer_relay_space,
    modify_application_pokt_space,
    modify_portal_pokt_space,
    increase_relay_fees_space,
    modify_servicer_pokt_space,
)
from typing import Tuple, Union
from ..classes import Servicer


def servicer_join_policy(
    state: StateType, params: ParamType, domain: Tuple[servicer_join_space]
) -> Tuple[servicer_entity_space]:
    space: servicer_join_space = domain[0]
    # Create entity
    servicer = Servicer(
        name=space["name"],
        servicer_salary=0,
        report_card=None,
        test_scores=None,
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
        service_url=space["service_url"],
        services=[],
        geo_zone=space["geo_zone"],
        operator_public_key=space["operator_public_key"],
        pause_height=None,
        stake_status="Staked",
        unstaking_height=None,
    )
    return ({"servicer": servicer},)


def servicer_relay_policy(
    state: StateType, params: ParamType, domain: Tuple[servicer_relay_space]
) -> Tuple[
    Union[modify_portal_pokt_space, modify_application_pokt_space],
    servicer_relay_space,
    modify_servicer_pokt_space,
    Union[servicer_relay_space, None],
]:
    # Payment from the requestor
    space1: Union[modify_portal_pokt_space, modify_application_pokt_space] = {}

    # Burn per relay policy
    space2: servicer_relay_space = {}

    # Relay fees to add
    space3: increase_relay_fees_space = {}

    # Payment to servicer
    space4: modify_servicer_pokt_space = {}

    # Space for if the session should be removed
    space5: Union[servicer_relay_space, None] = {}
