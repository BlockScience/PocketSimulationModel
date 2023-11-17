from ..types import StateType, ParamType
from ..spaces import (
    servicer_join_space,
    servicer_entity_space,
    servicer_relay_space,
    modify_application_pokt_space,
    modify_gateway_pokt_space,
    increase_relay_fees_space,
    modify_servicer_pokt_space,
    servicer_leave_space,
    servicer_stake_space,
)
from typing import Tuple, Union, List
from ..classes import Servicer


def servicer_join_policy(
    state: StateType, params: ParamType, domain: Tuple[servicer_join_space]
) -> Tuple[Union[servicer_entity_space, None]]:
    space: servicer_join_space = domain[0]
    # Create entity
    if space["stake_amount"] < params["minimum_stake_servicer"]:
        return (None,)
    else:
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
    Union[modify_gateway_pokt_space, modify_application_pokt_space],
    servicer_relay_space,
    Union[servicer_relay_space, None],
]:
    application = domain[0]["applications"]
    relay_charge = (
        domain[0]["session"]["number_of_relays"] * params["application_fee_per_relay"]
    )

    # Payment from the requestor
    if application.delegate:
        space1: modify_gateway_pokt_space = {
            "public_key": application.delegate,
            "amount": -relay_charge,
        }
    else:
        space1: modify_application_pokt_space = {
            "public_key": application,
            "amount": -relay_charge,
        }

    # Burn per relay policy
    space2: servicer_relay_space = domain[0]

    # Space for if the session should be removed
    space3: Union[servicer_relay_space, None] = domain[0]

    return (space1, space2, space3)


def servicer_leave_policy(
    state: StateType, params: ParamType, domain: Tuple[servicer_leave_space]
) -> Tuple[servicer_leave_space]:
    spaces1 = []
    spaces2 = []
    servicers = domain[0]["servicers"]
    for servicer in servicers:
        if servicers[servicer]:
            for service in servicer.services:
                spaces1.append(({"service": service, "servicer": servicer},))
            spaces2.append(({"servicer": servicer},))
    return (spaces1, spaces2)


def servicer_stake_policy(
    state: StateType, params: ParamType, domain: Tuple[servicer_stake_space]
) -> Tuple[modify_servicer_pokt_space, modify_servicer_pokt_space]:
    servicer = domain[0]["public_key"]
    amount = domain[0]["stake_amount"]
    space1: modify_servicer_pokt_space = {"amount": -amount, "public_key": servicer}
    space2: modify_servicer_pokt_space = {"amount": amount, "public_key": servicer}
    return (space1, space2)
