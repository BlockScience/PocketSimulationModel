from typing import NewType, TypedDict, List, Literal
from .Primitives import POKTType, PercentType, NanoSecondsType, GeoZoneType
from .Entity import (
    ApplicationEntityType,
    GatewayEntityType,
    ServiceEntityType,
    ServicerEntityType,
)
from .Data import SessionType

StateType = NewType(
    "State",
    TypedDict(
        "State",
        {
            "Geozones": List[GeoZoneType],
            "Applications": List[ApplicationEntityType],
            "DAO": object,
            "Gateways": List[GatewayEntityType],
            "Services": List[ServicerEntityType],
            "Servicers": List[ServiceEntityType],
            "Validators": List[object],
            "height": int,
            "day": int,
            "Sessions": List[SessionType],
        },
    ),
)

"""
    state["height"] = 0
    state["day"] = 0
    state["Treasury"] = None
    state["Sessions"] = []
    state["relay_fees"] = 0
    state["total_relays"] = None
    state["processed_relays"] = None
    state["pokt_price_true"] = 0.06 / 1e6
    state["pokt_price_oracle"] = 0.06 / 1e6
    state["n_transactions"] = None
    state["relay_log"] = None
    state["servicer_relay_log"] = None
    state["floating_supply"] = 1521517215 * 10e6
    state["understaked_servicers"] = []
    state["understaked_gateways"] = []
    state["understaked_applications"] = []
    state["POKT_burned"] = 0
    state["POKT_minted"] = 0
    state["period_slashing_costs"] = 0
    state["period_jailing_opportunity_cost"] = 0
"""


SystemParamsType = NewType(
    "SystemParams",
    TypedDict(
        "System Params",
        {
            "minimum_stake_servicer": List[POKTType],
            "minimum_stake_period_servicer": List[int],
            "minimum_pause_time": List[int],
            "max_chains_servicer": List[int],
            "relays_to_tokens_multiplier": List[POKTType],
            "slash_fraction_downtime": List[PercentType],
            "downtime_jail_duration": List[NanoSecondsType],
            "minimum_servicers_per_session": List[int],
            "maximum_servicers_per_session": List[int],
            "application_fee_per_relay": List[POKTType],
            "minimum_application_stake": List[POKTType],
            "app_burn_per_session": List[POKTType],
            "app_burn_per_relay": List[POKTType],
            "block_proposer_allocation": List[PercentType],
            "dao_allocation": List[PercentType],
            "servicer_allocation": List[PercentType],
            "stake_per_app_delegation": List[POKTType],
            "gateway_fee_per_relay": List[POKTType],
            "gateway_minimum_stake": List[POKTType],
            "session_token_bucket_coefficient": List[int],
            "dao_fee_percentage": List[PercentType],
            "validator_fee_percentage": List[PercentType],
            "transaction_fee": List[PercentType],
        },
    ),
)
BehaviorParamsType = NewType(
    "BehaviorParams",
    TypedDict(
        "Behavior Params",
        {
            "application_max_number": List[int],
            "servicer_max_number": List[int],
            "service_max_number": List[int],
            "gateway_max_number": List[int],
            "service_max_number_link": List[int],
            "application_leave_probability": List[float],
            "gateway_leave_probability": List[float],
            "service_leave_probability": List[float],
            "servicer_leave_probability": List[float],
            "service_unlinking_probability": List[float],
            "gateway_undelegation_probability": List[float],
            "relays_per_session_gamma_distribution_shape": List[float],
            "relays_per_session_gamma_distribution_scale": List[float],
            "average_session_per_application": List[int],
            "servicer_jailing_probability": List[float],
            "uses_gateway_probability": List[float],
            "applications_use_min_servicers": List[int],
            "applications_use_max_servicers": List[int],
            "lambda_ewm_revenue_expectation": List[float],
            "service_linking_probability_normal": List[float],
            "service_linking_probability_just_joined": List[float],
            "kick_bottom_probability": List[float],
        },
    ),
)
FunctionalParamsType = NewType(
    "FunctionalParams",
    TypedDict(
        "Functional Params",
        {
            "application_join_function": List[Literal["simple_unfiform"]],
            "servicer_join_function": List[Literal["simple_unfiform"]],
            "service_join_function": List[Literal["simple_unfiform"]],
            "gateway_join_function": List[Literal["simple_unfiform"]],
            "service_linking_function": List[Literal["test", "basic"]],
            "gateway_delegation_function": List[Literal["test", "basic"]],
            "relay_requests_function": List[Literal["test"]],
            "submit_relay_requests_function": List[Literal["test", "basic_gamma"]],
            "submit_relay_requests_policy_function": List[Literal["test", "V1"]],
            "application_leave_function": List[Literal["basic"]],
            "service_leave_function": List[Literal["basic"]],
            "servicer_leave_function": List[Literal["basic"]],
            "gateway_leave_function": List[Literal["basic"]],
            "service_unlinking_function": List[Literal["basic"]],
            "gateway_undelegation_function": List[Literal["basic"]],
            "servicer_stake_function": List[Literal["basic"]],
            "application_stake_function": List[Literal["basic"]],
            "jailing_function": List[Literal["basic"]],
            "gateway_stake_function": List[Literal["basic"]],
        },
    ),
)

ParamType = NewType("Params", TypedDict("Params", {}))
