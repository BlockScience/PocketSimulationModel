def s_update_servicers(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Servicers", state["Servicers"])


def p_servicers_join(_params, substep, state_history, state) -> dict:
    return {}


def p_relay_requests(_params, substep, state_history, state) -> dict:
    return {}


def p_jailing_slashing(_params, substep, state_history, state) -> dict:
    return {}


def p_servicers_leave(_params, substep, state_history, state) -> dict:
    return {}
