from ..types import StateType, ParamType
from ..spaces import servicer_join_space, servicer_entity_space
from typing import Tuple
from ..classes import Servicer


def servicer_join_policy(
    state: StateType, params: ParamType, domain: Tuple[servicer_join_space]
) -> Tuple[servicer_entity_space]:
    space: servicer_join_space = domain[0]
    # Create entity
    servicer = Servicer(
        name=space["name"],
        servicer_salary = 0,
        report_card = None,
        test_scores=None,
        pokt_holdings=space["personal_holdings"],
        staked_pokt=space["stake_amount"],
        service_url = space["service_url"],
        services=[],
        geo_zone=space["geo_zone"],
        operator_public_key = space["operator_public_key"],
        pause_height = None,
        stake_status="Staked",
        unstaking_height=None,
    )
    return ({"servicer": servicer},)