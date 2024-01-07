from ..action_chains import fee_reward_ac, block_reward_ac
import numpy as np
from model.config.events import event_map
import random
import dill
from ..policy import service_join_policy
from ..mechanisms import add_service


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


def p_update_price(_params, substep, state_history, state) -> dict:
    oracle_distortion = None

    # Hold it in the DAO because we don't have much of a choice of where else to hold
    if state["timestep"] == 0:
        with open("configuration_data/kde_oracle_returns.pkl", "rb") as file:
            kde_oracle_returns = dill.load(file)
            kde_oracle_returns.set_bandwidth(_params["oracle_price_kde_bandwidth"])
            state["DAO"].kde = kde_oracle_returns
    else:
        kde_oracle_returns = state["DAO"].kde

    if state["oracle_shutdown"]:
        pokt_price_oracle = state["pokt_price_oracle"]
        if type(state["oracle_shutdown"]) == int:
            countdown = state["oracle_shutdown"] - 1
            if countdown == 0:
                return {
                    "pokt_price_oracle": pokt_price_oracle,
                    "oracle_shutdown": False,
                }
            else:
                return {
                    "pokt_price_oracle": pokt_price_oracle,
                    "oracle_shutdown": countdown,
                }

    else:
        pokt_price_oracle = state["pokt_price_oracle"]
        # Find number of interarrivals and change oracle based upon
        if state["oracle_distortion"]:
            oracle_distortion = state["oracle_distortion"]
            oracle_distortion["time"] -= 1

        for _ in range(np.random.poisson(1 / _params["oracle_interarrival_time_mean"])):
            if oracle_distortion:
                pokt_price_oracle = (
                    np.exp(
                        np.random.normal(
                            oracle_distortion["mu"], oracle_distortion["sigma"]
                        )
                    )
                    * pokt_price_oracle
                )

            else:
                pokt_price_oracle = (
                    1 + kde_oracle_returns.resample(1)[0][0]
                ) * pokt_price_oracle

        if oracle_distortion:
            if oracle_distortion["time"] == 0:
                oracle_distortion = None

    return {
        "pokt_price_oracle": pokt_price_oracle,
        "oracle_distortion": oracle_distortion,
    }


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
        cap_relays_rttm = min(
            max(relays_per_day, _params["servicer_bootstrap_unwind_start"]),
            _params["servicer_bootstrap_end"],
        )
        b_rttm = (
            _params["maturity_relay_cost"] / (state["pokt_price_oracle"] * 1e6)
        ) - a_rttm * _params["servicer_bootstrap_end"]

        rttm_uncap = (a_rttm * cap_relays_rttm + b_rttm) * 1e6
        rttm_cap = (_params["supply_grow_cap"] * state["floating_supply"]) / (
            relays_per_day * 1000000000 * 365.2
        ) * 1e6 + gfpr

        if uses_supply_growth:
            rttm = min(rttm_uncap, rttm_cap)
        else:
            rttm = rttm_uncap

        return {"relays_to_tokens_multiplier": rttm}
    else:
        assert False, "Not implemented"


def s_update_gfpr(_params, substep, state_history, state, _input) -> tuple:
    return ("gateway_fee_per_relay", _input["gateway_fee_per_relay"])


def s_update_rttm(_params, substep, state_history, state, _input) -> tuple:
    return ("relays_to_tokens_multiplier", _input["relays_to_tokens_multiplier"])


def p_events(_params, substep, state_history, state) -> dict:
    if _params["event"]:
        event = event_map[_params["event"]]
        if event["time"] == state["timestep"]:
            if event["type"] == "servicer_shutdown":
                if event["attribute"] == "geozone":
                    if event["attribute_value"] == "random":
                        geo_zone = random.choice(state["Geozones"])
                        for servicer in state["Servicers"]:
                            if servicer.geo_zone == geo_zone:
                                servicer.shut_down = True
                    else:
                        assert False, "not implemented"
                else:
                    assert False, "not implemented"
            elif event["type"] == "service_shutdown":
                if event["service"] == "random":
                    service = random.choice(state["Services"])
                    service.shutdown = True
                else:
                    assert False, "Not implemented"
            elif event["type"] == "service_join":
                spaces = (
                    {"name": "ABC", "gateway_api_prefix": "ABC", "service_id": "ABC"},
                )
                spaces = service_join_policy(state, _params, spaces)
                add_service(state, _params, spaces)
            elif event["type"] == "service_relay_multiply":
                n_services = event["num_services"]
                multiple = event["multiple"]
                s = random.choices(state["Services"], k=n_services)
                for si in s:
                    state["relay_multiplier"][si] = multiple
            elif event["type"] == "oracle_shutdown":
                return {"oracle_shutdown": True}
            elif event["type"] == "oracle_delay_constant":
                return {"oracle_shutdown": event["delay_time"]}
            elif event["type"] == "oracle_distortion_constant":
                return {
                    "oracle_distortion": {
                        "time": event["delay_time"],
                        "mu": event["mu"],
                        "sigma": event["sigma"],
                    }
                }
            else:
                assert False, "not implemented"
        elif event["type"] == "service_shutdown":
            if event["time"] + event["shutdown_time"] == state["timestep"]:
                for service in state["Services"]:
                    service.shutdown = False
        return {}

    else:
        return {}


def s_relay_multiplier(_params, substep, state_history, state, _input) -> tuple:
    return ("relay_multiplier", state["relay_multiplier"])


def s_oracle_shutdown(_params, substep, state_history, state, _input) -> tuple:
    if "oracle_shutdown" in _input:
        return ("oracle_shutdown", _input["oracle_shutdown"])
    else:
        return ("oracle_shutdown", state["oracle_shutdown"])


def s_oracle_distortion(_params, substep, state_history, state, _input) -> tuple:
    if "oracle_distortion" in _input:
        return ("oracle_distortion", _input["oracle_distortion"])
    else:
        return ("oracle_distortion", state["oracle_distortion"])


def s_update_afpr(_params, substep, state_history, state, _input) -> tuple:
    if type(_params["application_fee_per_relay"]) in [float, int]:
        return ("application_fee_per_relay", _params["application_fee_per_relay"])
    else:
        multiplier = float(_params["application_fee_per_relay"].replace("GFPR*", ""))
        return (
            "application_fee_per_relay",
            _input["gateway_fee_per_relay"] * multiplier,
        )
