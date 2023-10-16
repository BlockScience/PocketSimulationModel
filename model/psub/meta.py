def p_update_time(_params, substep, state_history, state) -> dict:
    return {
        "height": state["height"] + 60 * 60 * 24,
        "day": state["day"] + 1,
    }


def s_update_height(_params, substep, state_history, state, _input) -> tuple:
    return ("height", _input["height"])


def s_update_day(_params, substep, state_history, state, _input) -> tuple:
    return ("day", _input["day"])
