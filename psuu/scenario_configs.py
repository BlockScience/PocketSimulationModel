from psuu.fitness_functions.gateway_viability import calc_gvs_thresh_ineq_met

scenario_configs = {}
scenario_configs["gateway_viability_sweep_ag"] = {
    "fitness_function": calc_gvs_thresh_ineq_met,
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
}
