from ..boundary_actions import fee_reward_ba, block_reward_ba
from ..policy import (
    fee_reward_policy,
    block_reward_policy_aggregate,
    assign_servicer_salary_policy,
    validator_block_reward_policy,
    dao_block_reward_policy,
)
from ..mechanisms import (
    decrease_relay_fees,
    modify_validator_pokt_holdings,
    modify_dao_pokt_holdings,
    modify_servicer_pokt_holdings,
    burn_pokt_mechanism,
    mint_pokt_mechanism,
)


def fee_reward_ac(state, params):
    spaces = fee_reward_ba(state, params)
    spaces = fee_reward_policy(state, params, spaces)
    for spaces_i in spaces[0]:
        modify_validator_pokt_holdings(state, params, spaces_i)
    modify_dao_pokt_holdings(state, params, spaces[1:2])


def update_revenue_expectations(state, params, servicer_earnings):
    lambda_ewm = params["lambda_ewm_revenue_expectation"]
    for servicer in state["Servicers"]:
        if servicer not in servicer_earnings:
            servicer_earnings[servicer] = {}
        last = servicer.revenue_expectations
        new = {}
        for service in servicer.services:
            val = servicer_earnings[servicer].get(service, 0)
            if service in last:
                new[service] = lambda_ewm * last[service] + (1 - lambda_ewm) * val
            else:
                new[service] = val
        servicer.revenue_expectations = new


def block_reward_ac(state, params):
    servicer_earnings = {}
    spaces = block_reward_ba(state, params)
    for spaces_i in spaces:
        spaces_i = block_reward_policy_aggregate(state, params, spaces_i)
        mint_pokt_mechanism(state, params, spaces_i[1:2])
        spaces_i2 = assign_servicer_salary_policy(
            state, params, spaces_i[:1], servicer_earnings
        )
        for spaces_j in spaces_i2:
            modify_servicer_pokt_holdings(state, params, spaces_j[:1])
            spaces_j[0]["public_key"].total_revenues += spaces_j[0]["amount"]
            burn_pokt_mechanism(state, params, spaces_j[1:2])
        spaces_i3 = validator_block_reward_policy(state, params, spaces_i[2:3])
        modify_validator_pokt_holdings(state, params, spaces_i3)
        spaces_i4 = dao_block_reward_policy(state, params, spaces_i[3:4])
        modify_dao_pokt_holdings(state, params, spaces_i4)
    update_revenue_expectations(state, params, servicer_earnings)
