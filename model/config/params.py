from copy import deepcopy

config_option_map = {"Test": {"System": "Test", "Behaviors": "Test"}}


def build_params(config_option):
    config_option = config_option_map[config_option]
    a = system_param_config[config_option["System"]]
    b = behavior_param_config[config_option["Behaviors"]]
    params = {**a, **b}

    params = deepcopy(params)
    return params


system_param_config = {
    "Test": {
        "minimum_stake_servicer": [None],
        "minimum_stake_period_servicer": [None],
        "minimum_pause_time": [None],
        "max_chains_servicer": [None],
        "salary_block_frequency": [None],
        "minimum_test_score_threshold": [None],
        "minimum_report_card_threshold": [None],
        "servicer_unbounding_period": [None],
        "relays_to_tokens_multiplier": [None],
        "slash_fraction_downtime": [None],
        "replay_attack_burn_multiplier": [None],
        "max_jailed_blocks": [None],
        "downtime_jail_duration": [None],
        "minimum_servicers_per_session": [None],
        "maximum_servicers_per_session": [None],
        "application_unstaking_time": [None],
        "application_fee_per_relay": [None],
        "minimum_application_stake": [None],
        "app_burn_per_session": [None],
        "app_burn_per_relay": [None],
        "block_proposer_allocation": [None],
        "stake_per_app_delegation": [None],
        "portal_fee_per_relay": [None],
        "portal_minimum_stake": [None],
        "portal_unstaking_time": [None],
        "session_block_frequency": [None],
        "session_token_bucket_coefficient": [None],
        "dao_fee_percentage": [None],
        "validator_fee_percentage": [None],
        "maturity_relay_cost": [None],
        "maturity_relay_charge": [None],
        "min_bootstrap_gateway_fee_per_relay": [None],
        "max_bootstrap_servicer_cost_per_relay": [None],
        "servicer_bootstrap_unwind_start": [None],
        "servicer_bootstrap_end": [None],
        "gateway_bootstrap_unwind_start": [None],
        "gateway_bootstrap_unwind_end": [None],
        "transaction_fee": [None],
        "supported_services": [None],
    }
}

behavior_param_config = {"Test": {}}