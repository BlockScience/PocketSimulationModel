def p_block_reward(_params, substep, state_history, state) -> tuple:
    return {}


def s_update_treasury(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Treasury", state["Treasury"])


def p_fee_reward(_params, substep, state_history, state) -> tuple:
    return {}
