from ..types import StateType, ParamType, ServiceEntityType
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
    servicer_pause_space2,
    burn_pokt_mechanism_space,
    jail_node_space,
    unjail_node_space,
)
from typing import Tuple, Union, List
from ..classes import Servicer
import random


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
            QoS=random.uniform(0.7, 1),
        )
        return ({"servicer": servicer},)


def servicer_relay_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[servicer_relay_space],
    relay_log,
    servicer_relay_log,
) -> Tuple[
    Union[modify_gateway_pokt_space, modify_application_pokt_space],
    servicer_relay_space,
    Union[servicer_relay_space, None],
]:
    application = domain[0]["applications"]

    # Log relays
    session = domain[0]["session"]
    n_relays = session["number_of_relays"]
    geo_zone = session["application"].geo_zone
    service = session["service"]
    key = (service, geo_zone)
    if key in relay_log:
        relay_log[key] += n_relays
    else:
        relay_log[key] = n_relays

    # Payment from the requestor
    if application.delegate:
        relay_charge = (
            domain[0]["session"]["number_of_relays"] * state["gateway_fee_per_relay"]
        )
        space1: modify_gateway_pokt_space = {
            "public_key": application.delegate,
            "amount": -relay_charge,
        }
    else:
        relay_charge = (
            domain[0]["session"]["number_of_relays"]
            * params["application_fee_per_relay"]
        )
        space1: modify_application_pokt_space = {
            "public_key": application,
            "amount": -relay_charge,
        }

    # Log which servicers did which work, modulo added to the first
    split_relays = n_relays // len(session["servicers"])
    modulo_relays = n_relays % len(session["servicers"])
    for i in range(len(session["servicers"])):
        amt = split_relays
        if i == 0:
            amt += modulo_relays
        s = session["servicers"][i]
        if s in servicer_relay_log:
            servicer_relay_log[s] += amt
        else:
            servicer_relay_log[s] = amt

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


def jail_node_policy(
    state: StateType, params: ParamType, domain: Tuple[jail_node_space]
) -> Tuple[
    servicer_pause_space2, modify_servicer_pokt_space, burn_pokt_mechanism_space
]:
    burn_stake = (
        domain[0]["node_address"].staked_pokt * params["slash_fraction_downtime"]
    )
    space1: servicer_pause_space2 = {
        "actor_type": ServiceEntityType,
        "address": domain[0]["node_address"],
        "caller_address": None,
        "signer": None,
        "height": state["height"],
    }
    space2: modify_servicer_pokt_space = {
        "amount": -burn_stake,
        "public_key": domain[0]["node_address"],
    }
    space3: burn_pokt_mechanism_space = {"burn_amount": burn_stake}

    return (space1, space2, space3)


def unjail_policy(
    state: StateType, params: ParamType, domain: Tuple[unjail_node_space]
) -> Tuple[Union[servicer_pause_space2, None]]:
    servicer = domain[0]["node_address"]
    delta_height = state["height"] - servicer.pause_height
    if delta_height >= params["minimum_pause_time"]:
        # Height is none to turn off pause height
        return (
            {
                "actor_type": "Servicer",
                "address": servicer,
                "caller_address": None,
                "height": None,
                "signer": None,
            },
        )
    else:
        return (None,)
