import numpy as np


def p_update_time(_params, substep, state_history, state) -> dict:
    return {
        "height": state["height"] + 60 * 60 * 24,
        "day": state["day"] + 1,
    }


def s_update_height(_params, substep, state_history, state, _input) -> tuple:
    return ("height", _input["height"])


def s_update_day(_params, substep, state_history, state, _input) -> tuple:
    return ("day", _input["day"])


def p_transactions(_params, substep, state_history, state) -> dict:
    return {"n_transactions": np.random.normal(300000, 15000)}


def s_update_n_transactions(_params, substep, state_history, state, _input) -> tuple:
    return ("n_transactions", _input["n_transactions"])


def s_update_relay_log(_params, substep, state_history, state, _input) -> tuple:
    return ("relay_log", _input["relay_log"])


def s_update_servicer_relay_log(
    _params, substep, state_history, state, _input
) -> tuple:
    return ("servicer_relay_log", _input["servicer_relay_log"])
