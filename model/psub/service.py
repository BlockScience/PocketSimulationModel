def s_update_services(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Services", state["Services"])


def p_service_linking(_params, substep, state_history, state) -> tuple:
    return {}


def p_service_join(_params, substep, state_history, state) -> tuple:
    return {}


def p_service_unlinking(_params, substep, state_history, state) -> tuple:
    return {}


def p_service_leave(_params, substep, state_history, state) -> tuple:
    return {}
