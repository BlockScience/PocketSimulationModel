from ..action_chains import portal_join_ac

def p_portal_join(_params, substep, state_history, state) -> tuple:
    portal_join_ac(state, _params)
    return {}


def s_update_portals(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Portals", state["Portals"])


def p_portal_leave(_params, substep, state_history, state) -> tuple:
    return {}
