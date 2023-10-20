from ..action_chains import service_join_ac, service_linking_ac

def s_update_services(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Services", state["Services"])


def p_service_linking(_params, substep, state_history, state) -> tuple:
    for servicer in state["Servicers"]:
        service_linking_ac(state, _params, servicer)
    return {}


def p_service_join(_params, substep, state_history, state) -> tuple:
    service_join_ac(state, _params)
    return {}


def p_service_unlinking(_params, substep, state_history, state) -> tuple:
    return {}


def p_service_leave(_params, substep, state_history, state) -> tuple:
    return {}
