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
        kpi_e[key] = np.exp(-slashing_cost / jailing_cost)
    return pd.Series(kpi_e)


def compute_kpi_14(unique_servicers):
    # Add in KPI 14, average slashing
    kpi_14 = {}
    for key in unique_servicers:
        servicers = unique_servicers[key]
        for servicer in servicers.values():
            servicer.kpi_14 = (
                servicer.staked_pokt_total_inflow / servicer.total_revenues
            )
        temp = [x.kpi_14 for x in servicers.values()]
        kpi_14[key] = sum(temp) / len(temp)
    return pd.Series(kpi_14)


def create_simulation_kpis(df):
    # Get unique servicers
    unique_servicers = get_unique_servicers(df)

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
    simulation_kpis["KPI 14"] = compute_kpi_14(unique_servicers)

    return simulation_kpis
