from ..action_chains import (
    application_join_ac,
    gateway_delegation_ac,
    application_leave_ac,
    gateway_undelegation_ac,
    application_stake_ac,
)


def p_application_join(_params, substep, state_history, state) -> tuple:
    application_join_ac(state, _params)
    return {}


def s_update_applications(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Applications", state["Applications"])


def p_gateway_delegation(_params, substep, state_history, state) -> tuple:
    for application in state["Applications"]:
        gateway_delegation_ac(state, _params, application)
    return {}


def p_gateway_undelegation(_params, substep, state_history, state) -> tuple:
    for application in state["Applications"]:
        gateway_undelegation_ac(state, _params, application)
    return {}


def p_application_leave(_params, substep, state_history, state) -> tuple:
    application_leave_ac(state, _params)
    understaked_applications = [
        x
        for x in state["Applications"]
        if x.staked_pokt < _params["minimum_application_stake"]
    ]
    return {"understaked_applications": understaked_applications}


def p_application_stake(_params, substep, state_history, state) -> tuple:
    application_stake_ac(state, _params)
    return {}


def s_update_understaked_applications(
    _params, substep, state_history, state, _input
) -> tuple:
    return ("understaked_applications", _input["understaked_applications"])
