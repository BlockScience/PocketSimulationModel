def p_application_join(_params, substep, state_history, state) -> tuple:
    return {}


def s_update_applications(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Applications", state["Applications"])
