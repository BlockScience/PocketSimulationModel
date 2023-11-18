from ..boundary_actions import fee_reward_ba, block_reward_ba
from ..policy import (
    fee_reward_policy,
    block_reward_policy_aggregate,
    assign_servicer_salary_policy,
)
from ..mechanisms import (
    decrease_relay_fees,
    modify_validator_pokt_holdings,
    modify_dao_pokt_holdings,
    modify_servicer_pokt_holdings,
    burn_pokt_mechanism,
)


def fee_reward_ac(state, params):
    spaces = fee_reward_ba(state, params)
    spaces = fee_reward_policy(state, params, spaces)
    for spaces_i in spaces[0]:
        modify_validator_pokt_holdings(state, params, spaces_i)
    modify_dao_pokt_holdings(state, params, spaces[1:2])


def block_reward_ac(state, params):
    spaces = block_reward_ba(state, params)
    for spaces_i in spaces:
        spaces_i = block_reward_policy_aggregate(state, params, spaces_i)
        spaces_i2 = assign_servicer_salary_policy(state, params, spaces_i[:1])
        for spaces_j in spaces_i2:
            modify_servicer_pokt_holdings(state, params, spaces_j[:1])
            burn_pokt_mechanism(state, params, spaces_j[1:2])
