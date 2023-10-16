def s_update_servicers(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Servicers", state["Servicers"])


def p_servicers_join(_params, substep, state_history, state) -> tuple:
    return {}
