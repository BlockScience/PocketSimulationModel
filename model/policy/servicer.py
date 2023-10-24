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
from typing import Tuple, Union, List
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
    increase_relay_fees_space,
    List[modify_servicer_pokt_space],
    Union[servicer_relay_space, None],
]:
    application = domain[0]["applications"]
    relay_payment = 100
    fees_charged = 10
    total_charge = relay_payment + fees_charged

    # Payment from the requestor
    if application.delegate:
        space1: modify_portal_pokt_space = {
            "public_key": application.delegate,
            "amount": -total_charge,
        }
    else:
        space1: modify_application_pokt_space = {
            "public_key": application,
            "amount": -total_charge,
        }

    # Burn per relay policy
    space2: servicer_relay_space = domain[0]

    # Relay fees to add
    space3: increase_relay_fees_space = {"POKT Amount": fees_charged}

    # Payment to servicer
    relay_payment2 = relay_payment / len(domain[0]["servicers"])
    space4: List[modify_servicer_pokt_space] = [
        (
            {
                "amount": relay_payment2,
                "public_key": x,
            },
        )
        for x in domain[0]["servicers"]
    ]

    # Space for if the session should be removed
    space5: Union[servicer_relay_space, None] = domain[0]

    return (space1, space2, space3, space4, space5)


servicer_leave_policy
