from ..types import StateType, ParamType
from ..spaces import portal_join_space, portal_entity_space, portal_leave_space
from typing import Tuple, Union
from ..classes import Portal


def portal_join_policy(
    state: StateType, params: ParamType, domain: Tuple[portal_join_space]
) -> Tuple[Union[portal_entity_space, None]]:
    space: portal_join_space = domain[0]

    # Need at least enough stake for one delegation
    if space["stake_amount"] < params["portal_minimum_stake"]:
        return (None,)

    # Create entity
    portal = Portal(
        name=space["name"],
        stake_status="Staked",
        delegators=[],
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
    )
    return ({"portal": portal},)


def portal_leave_policy(
    state: StateType, params: ParamType, domain: Tuple[portal_leave_space]
) -> Tuple[portal_leave_space]:
    return domain
