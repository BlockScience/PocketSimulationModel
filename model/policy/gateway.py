from ..types import StateType, ParamType
from ..spaces import gateway_join_space, gateway_entity_space, gateway_leave_space
from typing import Tuple, Union
from ..classes import Gateway


def gateway_join_policy(
    state: StateType, params: ParamType, domain: Tuple[gateway_join_space]
) -> Tuple[Union[gateway_entity_space, None]]:
    space: gateway_join_space = domain[0]

    # Need at least enough stake for one delegation
    if space["stake_amount"] < params["gateway_minimum_stake"]:
        return (None,)

    # Create entity
    gateway = Gateway(
        name=space["name"],
        stake_status="Staked",
        delegators=[],
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
    )
    return ({"gateway": gateway},)


def gateway_leave_policy(
    state: StateType, params: ParamType, domain: Tuple[gateway_leave_space]
) -> Tuple[gateway_leave_space]:
    return domain
