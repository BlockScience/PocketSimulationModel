from ..action_chains import fee_reward_ac, block_reward_ac
import numpy as np


def p_block_reward(_params, substep, state_history, state) -> tuple:
    block_reward_ac(state, _params)
    return {}


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
        np.random.normal(0.00332054298962304, 0.06562764398482432) + 1
    ) * state["pokt_price_true"]
    pokt_price_oracle = (
        0.95 * state["pokt_price_oracle"]
        + (pokt_price_true + np.random.normal(0, 0.03) * pokt_price_true) * 0.05
    )
    return {"pokt_price_true": pokt_price_true, "pokt_price_oracle": pokt_price_oracle}


def s_update_pokt_price_true(_params, substep, state_history, state, _input) -> tuple:
    return ("pokt_price_true", _input["pokt_price_true"])


def s_update_pokt_price_oracle(_params, substep, state_history, state, _input) -> tuple:
    return ("pokt_price_oracle", _input["pokt_price_oracle"])


def p_update_gfpr(_params, substep, state_history, state) -> dict:
    if type(_params["gateway_fee_per_relay"]) in [float, int]:
        return {"gateway_fee_per_relay": _params["gateway_fee_per_relay"]}
    elif _params["gateway_fee_per_relay"] == "Dynamic":
        a_gfpr = (
            (
                _params["min_bootstrap_gateway_fee_per_relay"]
                - _params["maturity_relay_charge"]
            )
            * (1 / (state["pokt_price_oracle"] * 1e6))
            / (
                _params["gateway_bootstrap_unwind_start"]
                - _params["gateway_bootstrap_end"]
            )
        )

        b_gfpr = (
            _params["maturity_relay_charge"] * (1 / (state["pokt_price_oracle"] * 1e6))
            - a_gfpr * _params["gateway_bootstrap_end"]
        )

        # If it is the first timestep we don't have relays completed yet
        # And convert to billions for the unit
        if state["processed_relays"]:
            relays_per_day = state["processed_relays"] / 1000000000
        else:
            relays_per_day = 1
        cap_relays_gfpr = min(
            max(relays_per_day, _params["gateway_bootstrap_unwind_start"]),
            _params["gateway_bootstrap_end"],
        )
        gfpr = (a_gfpr * cap_relays_gfpr + b_gfpr) * 1e6
        return {"gateway_fee_per_relay": gfpr}
    else:
        assert False, "Not implemented"


def p_update_rttm(_params, substep, state_history, state) -> dict:
    if type(_params["relays_to_tokens_multiplier"]) in [float, int]:
        return {"relays_to_tokens_multiplier": _params["relays_to_tokens_multiplier"]}
    elif _params["relays_to_tokens_multiplier"] == "Dynamic":
        a_gfpr = (
            (
                _params["min_bootstrap_gateway_fee_per_relay"]
                - _params["maturity_relay_charge"]
            )
            * (1 / (state["pokt_price_oracle"] * 1e6))
            / (
                _params["gateway_bootstrap_unwind_start"]
                - _params["gateway_bootstrap_end"]
            )
        )

        b_gfpr = (
            _params["maturity_relay_charge"] * (1 / (state["pokt_price_oracle"] * 1e6))
            - a_gfpr * _params["gateway_bootstrap_end"]
        )

        # If it is the first timestep we don't have relays completed yet
        # And convert to billions for the unit
        if state["processed_relays"]:
            relays_per_day = state["processed_relays"] / 1000000000
        else:
            relays_per_day = 1
        cap_relays_gfpr = min(
            max(relays_per_day, _params["gateway_bootstrap_unwind_start"]),
            _params["gateway_bootstrap_end"],
        )
        gfpr = (a_gfpr * cap_relays_gfpr + b_gfpr) * 1e6

        uses_supply_growth = True

        a_rttm = (
            (
                _params["max_bootstrap_servicer_cost_per_relay"]
                - _params["maturity_relay_cost"]
            )
            / (state["pokt_price_oracle"] * 1e6)
            / (
                _params["servicer_bootstrap_unwind_start"]
                - _params["servicer_bootstrap_end"]
            )
        )
        print(a_rttm)
        cap_relays_rttm = 0
        b_rttm = (
            _params["maturity_relay_charge"] / (state["pokt_price_oracle"] * 1e6)
        ) - a_rttm * _params["servicer_bootstrap_end"]
        print(b_rttm)

        rttm_uncap = (a_rttm * cap_relays_rttm + b_rttm) * 1e6
        rttm_cap = (_params["supply_grow_cap"] * state["floating_supply"]) / (
            relays_per_day * 1000000000 * 365.2
        ) * 1e6 + gfpr

        if uses_supply_growth:
            rttm = min(rttm_uncap, rttm_cap)
        else:
            rttm = rttm_uncap
        print(rttm)
        return {"relays_to_tokens_multiplier": 100}
    else:
        assert False, "Not implemented"


def s_update_gfpr(_params, substep, state_history, state, _input) -> tuple:
    return ("gateway_fee_per_relay", _input["gateway_fee_per_relay"])


def s_update_rttm(_params, substep, state_history, state, _input) -> tuple:
    return ("relays_to_tokens_multiplier", _input["relays_to_tokens_multiplier"])
