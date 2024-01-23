import pandas as pd
from model.config.params import *
from .scenario_configs import scenario_configs

KPI_MAP = {
    "servicer_npv": "kpi_1",
    "gateway_npv": "kpi_3",
    "circulating_supply": "kpi_4",
    "available_supply": "kpi_5",
    "servicer_slashing_cost": "kpi_8",
    "dao_value_capture": "kpi_10",
    "servicer_jailing_cost": "kpi_11",
    "servicer_capital_costs": "kpi_14",
    "network_load_balancing": "kpi_C",
    "net_inflation": "kpi_D",
    "circulating_supply_available_supply_ratio": ["kpi_4", "kpi_5"],
    "net_inflation_dao_value_capture_elasticity": ["kpi_D", "kpi_10"],
}


# Note that these are meant to applied to subsets of the dataframe, i.e. do the grouping and then apply this
THRESHOLD_INEQUALITIES_MAP = {
    "servicer_npv": lambda df, threshold_parameters: threshold_mc_fraction(
        df, threshold_parameters["s1"], None, threshold_parameters["s2"], "servicer_npv"
    ),
    "servicer_capital_costs": lambda df, threshold_parameters: threshold_average(
        df,
        threshold_parameters["a1"],
        threshold_parameters["a2"],
        "servicer_capital_costs",
    ),
    "servicer_slashing_cost": lambda df, threshold_parameters: not threshold_mc_fraction(
        df,
        threshold_parameters["b1"],
        None,
        threshold_parameters["b2"],
        "servicer_slashing_cost",
    ),
    "servicer_jailing_cost": lambda df, threshold_parameters: not threshold_mc_fraction(
        df,
        threshold_parameters["c1"],
        None,
        threshold_parameters["c2"],
        "servicer_jailing_cost",
    ),
    "gateway_npv": lambda df, threshold_parameters: threshold_mc_fraction(
        df, threshold_parameters["t1"], None, threshold_parameters["t2"], "gateway_npv"
    ),
    "circulating_supply_available_supply_ratio": lambda df, threshold_parameters: threshold_kpi_ratios(
        df,
        threshold_parameters["v1"],
        None,
        "circulating_supply_available_supply_ratio",
    ),
    "net_inflation": lambda df, threshold_parameters: threshold_average(
        df, threshold_parameters["y1"], threshold_parameters["y2"], "net_inflation"
    ),
    "dao_value_capture": lambda df, threshold_parameters: threshold_mc_fraction(
        df,
        threshold_parameters["z1"],
        threshold_parameters["z2"],
        threshold_parameters["z3"],
        "dao_value_capture",
    ),
    "net_inflation_dao_value_capture_elasticity": lambda df, threshold_parameters: threshold_elasticity(
        df,
        threshold_parameters["x1"],
        threshold_parameters["x2"],
        "net_inflation_dao_value_capture_elasticity",
    ),
    "network_load_balancing": lambda df, min, max, frac: threshold_load_balancing(
        df, min, max, frac, "network_load_balancing"
    ),
}

KPI_CLEANUP_MAP = {
    "KPI 14": "kpi_14",
    "KPI 1": "kpi_1",
    "KPI 3": "kpi_3",
    "KPI D": "kpi_D",
    "KPI 8": "kpi_8",
}


def load_kpis(sweep):
    kpis = pd.read_csv("simulation_data/{}.csv".format(sweep), index_col=0)
    kpis = kpis.rename(columns=KPI_CLEANUP_MAP)
    kpis["kpi_4"] = kpis["circulating_supply"]
    kpis["kpi_5"] = kpis["floating_supply"]
    kpis["kpi_D"] = kpis["net_mint_rate_cummulative"]
    kpis["kpi_10"] = kpis["dao_value_capture"]
    kpis["kpi_11"] = kpis["KPI 11"]
    return kpis


def threshold_mc_fraction(df, min, max, frac, entity):
    if entity not in [
        "servicer_npv",
        "gateway_npv",
        "dao_value_capture",
        "servicer_slashing_cost",
        "servicer_jailing_cost",
    ]:
        raise ValueError("Error: unsupported threshold inequality type")

    num_monte_carlo_sims = len(df)
    kpi = KPI_MAP[entity]

    ineq = df[kpi]

    # Success criteria
    if min and max:
        ineq = (ineq > min) & (ineq < max)
    elif min and not max:
        ineq = ineq > min
    elif max and not min:
        ineq = ineq < max
    else:
        raise ValueError(
            "Error: must provide at least one maximum or minimum threshold value"
        )

    # Number of successful runs
    ineq = ineq.mean()

    # Successful fraction
    return ineq >= frac


def threshold_average(df, min, max, entity) -> float:
    if entity not in [
        "servicer_capital_costs",
        "net_inflation",
        "circulating_supply_available_supply_ratio",
        "net_inflation_dao_value_capture_elasticity",
    ]:
        raise ValueError("Error: unsupported threshold inequality type")

    if "ratio" in entity:
        kpi = "ratio"
    elif "elasticity" in entity:
        kpi = "elasticity"
    else:
        kpi = KPI_MAP[entity]

    # Get average
    avg = df[kpi].mean()

    if min and max:
        return avg > min and avg < max
    elif min and not max:
        return avg > min
    elif max and not min:
        return avg < max
    else:
        raise ValueError(
            "Error: must provide at least one maximum or minimum threshold value"
        )


def threshold_kpi_ratios(df, min, max, entity):
    if entity not in ["circulating_supply_available_supply_ratio"]:
        raise ValueError("Error: unsupported threshold inequality type")

    # This must be a list with two KPI entries
    kpi = KPI_MAP[entity]

    df = df.copy()
    df["ratio"] = df[kpi[0]] / df[kpi[1]]

    return threshold_average(df, min, max, entity)


def threshold_elasticity(df, min, max, entity):
    if entity not in ["net_inflation_dao_value_capture_elasticity"]:
        raise ValueError("Error: unsupported threshold inequality type")

    kpi = KPI_MAP[entity]

    # df_delta = df.pct_change()
    # df_delta["elasticity"] = df_delta[kpi[0]] / df_delta[kpi[1]]
    # df.drop(df.index[:1], inplace=True)
    # df["elasticity"] = df_delta["elasticity"]

    df = df.copy()
    df["elasticity"] = df[kpi[0]] / df[kpi[1]]

    return threshold_average(df, min, max, entity)


def compute_threshold_inequalities(
    kpis, variable_params, threshold_parameters, threshold_inequalities
):
    grouping = kpis.groupby(["param_" + x for x in variable_params])
    df_thresholds = [
        grouping.apply(
            lambda x: THRESHOLD_INEQUALITIES_MAP[key](x, threshold_parameters)
        )
        for key in threshold_inequalities
    ]
    df_thresholds = pd.concat(df_thresholds, axis=1)
    df_thresholds.columns = [x + "_success" for x in threshold_inequalities]
    return df_thresholds


def load_sweep(sweep):
    sweep_family = sweep[: sweep.index("_ag") + 3]
    kpis = load_kpis(sweep)
    param_config = globals()[sweep]
    next_name = sweep[:-2] + str(int(sweep[-2]) + 1) + "_"
    variable_params = scenario_configs[sweep_family]["variable_params"]
    control_params = scenario_configs[sweep_family]["control_params"]
    threshold_inequalities = scenario_configs[sweep_family]["threshold_inequalities"]
    threshold_parameters = scenario_configs[sweep_family]["threshold_parameters"]

    return (
        sweep_family,
        kpis,
        param_config,
        next_name,
        variable_params,
        control_params,
        threshold_inequalities,
        threshold_parameters,
    )
