from ..action_chains import (
    servicer_join_ac,
    relay_requests_ac,
    servicer_leave_ac,
    servicers_stake_ac,
    jailing_slashing_ac,
)


def s_update_servicers(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Servicers", state["Servicers"])


def p_servicers_join(_params, substep, state_history, state) -> dict:
    servicer_join_ac(state, _params)
    return {}


def p_relay_requests(_params, substep, state_history, state) -> dict:
    number_relays = _params["average_session_per_application"] * len(
        state["Applications"]
    )
    total_relays = 0
    processed_relays = 0
    relay_log = {}
    for _ in range(number_relays):
        out = relay_requests_ac(state, _params, relay_log)
        total_relays += out["total_relays"]
        processed_relays += out["processed_relays"]
    return {
        "total_relays": total_relays,
        "processed_relays": processed_relays,
        "relay_log": relay_log,
    }


def p_jailing_slashing(_params, substep, state_history, state) -> dict:
    jailing_slashing_ac(state, _params)
    return {}


def p_servicers_leave(_params, substep, state_history, state) -> dict:
    servicer_leave_ac(state, _params)
    return {}


def p_servicers_stake(_params, substep, state_history, state) -> dict:
    servicers_stake_ac(state, _params)
    return {}
