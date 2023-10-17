def s_update_validators(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Validators", state["Validators"])
