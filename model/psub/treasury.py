from ..action_chains import fee_reward_ac
import numpy as np


def p_block_reward(_params, substep, state_history, state) -> tuple:
    return {}


def s_update_treasury(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("Treasury", state["Treasury"])


def p_fee_reward(_params, substep, state_history, state) -> tuple:
    fee_reward_ac(state, _params)
    return {}


def s_update_total_relays(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("total_relays", _input["total_relays"])


def s_update_processed_relays(_params, substep, state_history, state, _input) -> tuple:
    # Pass through because they are updated by reference
    return ("processed_relays", _input["processed_relays"])


def p_update_price(_params, substep, state_history, state) -> tuple:
    pokt_price_true = (
        np.random.normal(0.00332054298962304, 0.06562764398482432)
        * state["pokt_price_true"]
    )
    pokt_price_oracle = (
        0.95 * state["pokt_price_oracle"]
        + (pokt_price_true + np.random.normal(0, 0.03) * pokt_price_true) * 0.05
    )
    return {"pokt_price_true": pokt_price_true, "pokt_price_oracle": pokt_price_oracle}


def s_update_pokt_price_true(_params, substep, state_history, state, _input) -> tuple:
    return ("pokt_price_true", _input["pokt_price_true"])


def s_update_pokt_price_oracle(_params, substep, state_history, state, _input) -> tuple:
    return ("pokt_price_oracle", _input["pokt_price_oracle"])
