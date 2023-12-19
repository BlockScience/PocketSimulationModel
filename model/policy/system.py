from ..types import StateType, ParamType
from ..spaces import (
    distribute_fees_space,
    decrease_relay_fees_space,
    modify_validator_pokt_space,
    modify_dao_pokt_space,
    mint_block_rewards_space,
    assign_servicer_salary_space,
    mint_pokt_mechanism_space,
    validator_block_reward_space,
    dao_block_reward_space,
    modify_servicer_pokt_space,
    burn_pokt_mechanism_space,
)
from typing import Tuple, List
from math import isclose


def fee_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[distribute_fees_space]
) -> Tuple[List[modify_validator_pokt_space], modify_dao_pokt_space]:
    accumulated_fees = state["n_transactions"] * params["transaction_fee"]
    validator_share = accumulated_fees * params["validator_fee_percentage"]
    dao_share = accumulated_fees * params["dao_fee_percentage"]
    assert isclose(accumulated_fees, validator_share + dao_share)

    # space1: decrease_relay_fees_space = {"POKT Amount": accumulated_fees}
    space1: List[modify_validator_pokt_space] = [
        ({"public_key": state["Validators"][0], "amount": validator_share},)
    ]
    space2: modify_dao_pokt_space = {"amount": dao_share}

    return (space1, space2)


def block_reward_policy_aggregate(
    state: StateType, params: ParamType, domain: Tuple[mint_block_rewards_space]
) -> Tuple[
    assign_servicer_salary_space,
    mint_pokt_mechanism_space,
    validator_block_reward_space,
    dao_block_reward_space,
]:
    space = domain[0]

    reward = int(space["relays"] * state["relays_to_tokens_multiplier"])

    space1: assign_servicer_salary_space = {
        "geo_zone": space["geo_zone"],
        "reward": reward * params["servicer_allocation"],
        "service": space["service"],
    }

    space2: mint_pokt_mechanism_space = {"mint_amount": reward}
    space3: validator_block_reward_space = {
        "public_key": space["block_producer"],
        "reward_amount": reward * params["block_proposer_allocation"],
    }
    space4: dao_block_reward_space = {
        "reward_amount": reward * params["dao_allocation"]
    }
    return (space1, space2, space3, space4)


def assign_servicer_salary_policy(
    state: StateType,
    params: ParamType,
    domain: Tuple[assign_servicer_salary_space],
    servicer_earnings,
) -> List[Tuple[modify_servicer_pokt_space, burn_pokt_mechanism_space]]:
    space = domain[0]
    service = space["service"]
    servicers = service.servicers
    geo_servicers = [
        x for x in servicers if x.geo_zone == space["geo_zone"] and not x.pause_height
    ]
    if len(geo_servicers) > 0:
        servicers = geo_servicers
    # This is probably a bad failsafe
    if len(geo_servicers) == 0:
        servicers = [x for x in state["Servicers"] if not x.pause_height]
    out = []
    payment_per = space["reward"] // len(servicers)
    for servicer in servicers:
        if servicer not in servicer_earnings:
            servicer_earnings[servicer] = {}
        if service not in servicer_earnings[servicer]:
            servicer_earnings[servicer][service] = payment_per
        else:
            servicer_earnings[servicer][service] += payment_per

        space1: modify_servicer_pokt_space = {
            "amount": payment_per * servicer.QoS,
            "public_key": servicer,
        }
        space2: burn_pokt_mechanism_space = {
            "burn_amount": payment_per * (1 - servicer.QoS)
        }
        out.append((space1, space2))
    return out


def validator_block_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[validator_block_reward_space]
) -> Tuple[modify_validator_pokt_space]:
    out: modify_validator_pokt_space = {
        "amount": domain[0]["reward_amount"],
        "public_key": domain[0]["public_key"],
    }
    return (out,)


def dao_block_reward_policy(
    state: StateType, params: ParamType, domain: Tuple[dao_block_reward_space]
) -> Tuple[modify_dao_pokt_space]:
    out: modify_dao_pokt_space = {"amount": domain[0]["reward_amount"]}
    return (out,)
