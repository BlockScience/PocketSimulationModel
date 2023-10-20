from ..types import StateType, ParamType
from ..spaces import portal_join_space, portal_entity_space
from typing import Tuple
from ..classes import Portal


def portal_join_policy(
    state: StateType, params: ParamType, domain: Tuple[portal_join_space]
) -> Tuple[portal_entity_space]:
    space: portal_join_space = domain[0]
    # Create entity
    portal = Portal(
        name=space["name"],
        stake_status="Staked",
        delegators = [],
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
    )
    return ({"portal": portal},)