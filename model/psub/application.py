from ..action_chains import application_join_ac


def p_application_join(_params, substep, state_history, state) -> tuple:
    application_join_ac(state, _params)
    return {}


def s_update_applications(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Applications", state["Applications"])


def p_portal_delegation(_params, substep, state_history, state) -> tuple:
    return {}


def p_portal_undelegation(_params, substep, state_history, state) -> tuple:
    return {}


def p_application_leave(_params, substep, state_history, state) -> tuple:
    return {}
