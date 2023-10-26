from ..action_chains import (
    application_join_ac,
    portal_delegation_ac,
    application_leave_ac,
    portal_undelegation_ac,
)


def p_application_join(_params, substep, state_history, state) -> tuple:
    application_join_ac(state, _params)
    return {}


def s_update_applications(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Applications", state["Applications"])


def p_portal_delegation(_params, substep, state_history, state) -> tuple:
    for application in state["Applications"]:
        portal_delegation_ac(state, _params, application)
    return {}


def p_portal_undelegation(_params, substep, state_history, state) -> tuple:
    portal_undelegation_ac(state, _params)
    return {}


def p_application_leave(_params, substep, state_history, state) -> tuple:
    application_leave_ac(state, _params)
    return {}
