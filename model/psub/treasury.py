from ..action_chains import fee_reward_ac


def p_block_reward(_params, substep, state_history, state) -> tuple:
    return {}


def s_update_treasury(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Treasury", state["Treasury"])


def p_fee_reward(_params, substep, state_history, state) -> tuple:
    fee_reward_ac(state, _params)
    return {}


def s_update_total_relays(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("total_relays", _input["total_relays"])


def s_update_processed_relays(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("processed_relays", _input["processed_relays"])
