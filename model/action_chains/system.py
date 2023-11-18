from ..boundary_actions import fee_reward_ba, block_reward_ba
from ..policy import fee_reward_policy
from ..mechanisms import (
    decrease_relay_fees,
    modify_validator_pokt_holdings,
    modify_dao_pokt_holdings,
)


def fee_reward_ac(state, params):
    spaces = fee_reward_ba(state, params)
    spaces = fee_reward_policy(state, params, spaces)
    for spaces_i in spaces[0]:
        modify_validator_pokt_holdings(state, params, spaces_i)
    modify_dao_pokt_holdings(state, params, spaces[1:2])


def block_reward_ac(state, params):
    spaces = block_reward_ba(state, params)
