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
