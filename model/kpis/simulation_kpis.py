import pandas as pd
from ..config.params import build_params
import numpy as np


def get_unique_servicers(df):
    unique_servicers = {}
    # Iterate through the simulations
    for key in df["key"].unique():
        # Assign as the last of timestep with one
        unique_servicers[key] = {}
        df_mini = df[df["key"] == key]
        for x in df_mini["Servicers"]:
            for y in x:
                unique_servicers[key][y.id_number] = y
    return unique_servicers


def get_unique_gateways(df):
    unique_gateways = {}
    # Iterate through the simulations
    for key in df["key"].unique():
        # Assign as the last of timestep with one
        unique_gateways[key] = {}
        df_mini = df[df["key"] == key]
        for x in df_mini["Gateways"]:
            for y in x:
                unique_gateways[key][y.id_number] = y
    return unique_gateways


def compute_kpi8(unique_servicers):
    # Add in KPI 8, average slashing
    kpi8 = {}
    for key in unique_servicers:
        servicers = unique_servicers[key]
        slashes = [
            sum(x.slashing_history.values())
            for x in servicers.values()
            if len(x.slashing_history) > 0
        ]
        n = len(slashes)
        total_slashed = -sum(slashes)
        if n > 0:
            kpi8[key] = total_slashed / n
        else:
            kpi8[key] = None
    kpi8 = pd.Series(kpi8)
    return kpi8


def compute_kpi_e(unique_servicers):
    # Add in KPI E, average slashing
    kpi_e = {}
    for key in unique_servicers:
        servicers = unique_servicers[key]
        slashing_cost = sum(
            [sum(x.slashing_history.values()) for x in servicers.values()]
        )
        jailing_cost = -sum(
            [
                sum(x.jail_lost_revenue_history.values())
                + sum(x.slashing_history.values())
                for x in servicers.values()
            ]
        )
        if jailing_cost > 0:
            kpi_e[key] = np.exp(-slashing_cost / jailing_cost)
        else:
            kpi_e[key] = None
    return pd.Series(kpi_e)


def compute_kpi3(unique_gateways, simulation_kpis, r=0.05):
    # Add in KPI 3
    kpi3 = {}
    for key in unique_gateways:
        gateways = unique_gateways[key].values()
        average_stake = sum([x.staked_pokt for x in gateways]) / len(gateways)
        for gateway in gateways:
            """gateway.kpi3 = (
                gateway.staked_pokt
                - average_stake
                - (1 + 1 / r) * gateway.fees_paid
                - (1 / r)
                * max(
                    0,
                    simulation_kpis.loc[key, "param_gateway_minimum_stake"]
                    - average_stake,
                )
            )"""

            # All is converted to POKT in this hence the 1e6
            Q = gateway.relays_served
            gateway.kpi3 = (1 + 1 / r) * (
                simulation_kpis.loc[key, "param_kpi_3_R"]
                - simulation_kpis.loc[key, "param_gateway_fee_per_relay"] / 1e6
            ) * Q - max(
                0,
                simulation_kpis.loc[key, "param_gateway_minimum_stake"] - average_stake,
            ) / 1e6
        vals = [x.kpi3 for x in gateways]
        kpi3[key] = sum(vals) / len(vals)

    kpi3 = pd.Series(kpi3)
    return kpi3


def compute_kpi_11(unique_servicers):
    # Add in KPI 11
    kpi_11 = {}
    for key in unique_servicers:
        servicers = unique_servicers[key]
        for servicer in servicers.values():
            if servicer.total_revenues > 0:
                servicer.kpi_11 = (
                    sum(servicer.jail_lost_revenue_history.values())
                    / servicer.total_revenues
                )
            else:
                servicer.kpi_11 = None
        temp = [x.kpi_11 for x in servicers.values() if x.kpi_11]
        if len(temp) > 0:
            kpi_11[key] = sum(temp) / len(temp)
        else:
            kpi_11[key] = None
    return pd.Series(kpi_11)


def compute_kpi_1(
    unique_servicers,
    simulation_kpis,
    r=0.05,
):
    kpi_1 = {}
    for key in unique_servicers:
        servicers = unique_servicers[key]
        for servicer in servicers.values():
            t = simulation_kpis.loc[key, "timestep"]
            p_j = (
                1
                - (1 - simulation_kpis.loc[key, "param_servicer_jailing_probability"])
                ** t
            )
            npv = (1 + 1 / r) * (
                servicer.total_revenues
                - r * servicer.staked_pokt
                + (
                    1
                    / (1 + r)
                    * (1 - p_j)
                    * sum(servicer.jail_lost_revenue_history.values())
                )
            )
            servicer.kpi_1 = npv

        temp = [x.kpi_1 for x in servicers.values() if x.kpi_1]
        if len(temp) > 0:
            kpi_1[key] = sum(temp) / len(temp)
        else:
            kpi_1[key] = None
    return pd.Series(kpi_1)


def compute_kpi_14(unique_servicers):
    # Add in KPI 14, average slashing
    kpi_14 = {}
    for key in unique_servicers:
        servicers = unique_servicers[key]
        for servicer in servicers.values():
            if servicer.total_revenues > 0:
                servicer.kpi_14 = (
                    servicer.staked_pokt_total_inflow / servicer.total_revenues
                )
            else:
                servicer.kpi_14 = None
        temp = [x.kpi_14 for x in servicers.values() if x.kpi_14]
        if len(temp) > 0:
            kpi_14[key] = sum(temp) / len(temp)
        else:
            kpi_14[key] = None
    return pd.Series(kpi_14)


def create_simulation_kpis(df):
    # Get unique servicers
    unique_servicers = get_unique_servicers(df)
    unique_gateways = get_unique_gateways(df)

    simulation_kpis = []

    # Minting rate
    simulation_kpis.append(
        df.groupby("key")["POKT_net_mint"].sum()
        / df.groupby("key")["floating_supply"].first()
    )

    # Average of KPI C
    simulation_kpis.append(df.groupby("key")["kpi_c"].mean())

    # Put the two together to start our dataframe
    simulation_kpis = pd.concat(simulation_kpis, axis=1)
    simulation_kpis.columns = ["Net Minting Rate", "KPI C"]

    # Add in metadata
    simulation_kpis = simulation_kpis.join(
        df.groupby(["key"])[
            ["Experiment Name", "State Set", "Params Set", "timestep"]
        ].last()
    )

    # Add the parameters in
    params = simulation_kpis["Params Set"].apply(build_params).apply(pd.Series)
    params.columns = "param_" + params.columns
    params = params.applymap(lambda x: x[0])
    simulation_kpis = simulation_kpis.join(params)
    # simulation_kpis["KPI 8"] = compute_kpi8(unique_servicers)
    simulation_kpis["KPI E"] = compute_kpi_e(unique_servicers)
    simulation_kpis["KPI 1"] = compute_kpi_1(
        unique_servicers,
        simulation_kpis,
    )
    simulation_kpis["KPI 3"] = compute_kpi3(unique_gateways, simulation_kpis)
    simulation_kpis["KPI 11"] = compute_kpi_11(unique_servicers)
    simulation_kpis["KPI 14"] = compute_kpi_14(unique_servicers)

    agg1 = df.groupby("key")[["total_relays", "processed_relays"]].sum()
    agg2 = df.groupby("key")[["kpi_a"]].mean()
    agg3 = df.groupby("key")[
        [
            "floating_supply",
            "circulating_supply",
            "dao_value_capture",
            "POKT_burned_cummulative",
            "POKT_minted_cummulative",
            "POKT_net_mint_cummulative",
            "burn_rate_cummulative",
            "mint_rate_cummulative",
            "net_mint_rate_cummulative",
        ]
    ].last()
    simulation_kpis = pd.concat([simulation_kpis, agg1, agg2, agg3], axis=1)

    return simulation_kpis
