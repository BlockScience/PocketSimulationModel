from typing import NewType, TypedDict, List
from .Primitives import POKTType, PercentType, NanoSecondsType

StateType = NewType("State", TypedDict("State", {}))

ParamType = NewType("Params", TypedDict("Params", {}))

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
FunctionalParamsType = NewType("FunctionalParams", TypedDict("Functional Params", {}))
