scenario_configs = {}
scenario_configs["gateway_viability_sweep_ag"] = {
    "variable_params": [
        "session_token_bucket_coefficient",
        "gateway_fee_per_relay",
        "application_fee_per_relay",
        "gateway_minimum_stake",
        "minimum_application_stake",
    ],
    "control_params": [
        "application_max_number",
        "relays_per_session_gamma_distribution_scale",
    ],
    "threshold_inequalities": ["servicer_npv", "servicer_capital_costs", "gateway_npv"],
    "threshold_parameters": {
        "a1": 0.1,
        "a2": 0.9,
        "s1": 750 * 1e6,
        "s2": 0.9,
        "t1": 7500 * 1e6,
        "t2": 0.9,
    },
}
scenario_configs["network_failures_oracle_ag"] = {
    "variable_params": [
        "relays_to_tokens_multiplier",
        "gateway_fee_per_relays",
        "application_fee_per_relay",
        "gateway_minimum_stake",
        "minimum_application_stake",
        "dao_allocation",
        "validator_fee_percentage",
    ],
    "control_params": ["oracle_treatment_time_mean", "event"],
    "threshold_inequalities": [
        "servicer_npv",
        "gateway_npv",
        "circulating_supply_available_supply_ratio",
        "net_inflation",
        "dao_value_capture",
    ],
    "threshold_parameters": {
        "s1": 750 * 1e6,
        "s2": 0.9,
        "t1": 7500 * 1e6,
        "t2": 0.9,
        "v1": 0.3 * 1e6,
        "y1": -0.1,
        "y2": 0.05,
        "z1": 0.02,
        "z2": 0.1,
        "z3": 0.9,
    },
}
