from ..action_chains import gateway_join_ac, gateway_leave_ac, gateway_stake_ac


def p_gateway_join(_params, substep, state_history, state) -> tuple:
    gateway_join_ac(state, _params)
    return {}


def s_update_gateways(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Gateways", state["Gateways"])


def p_gateway_leave(_params, substep, state_history, state) -> tuple:
    gateway_leave_ac(state, _params)
    return {}


def p_gateway_stake(_params, substep, state_history, state) -> tuple:
    gateway_stake_ac(state, _params)
    return {}
