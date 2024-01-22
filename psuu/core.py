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
    "servicer_slashing_cost": lambda df, min, max, frac: threshold_mc_fraction(
        df, min, max, frac, "servicer_slashing_cost"
    ),
    "servicer_jailing_cost": lambda df, min, max, frac: threshold_mc_fraction(
        df, min, max, frac, "servicer_jailing_cost"
    ),
    "gateway_npv": lambda df, threshold_parameters: threshold_mc_fraction(
        df, threshold_parameters["t1"], None, threshold_parameters["t2"], "gateway_npv"
    ),
    "circulating_supply_available_supply_ratio": lambda df, min, max: threshold_kpi_ratios(
        df, min, max, "circulating_supply_available_supply_ratio"
    ),
    "net_inflation": lambda df, min, max: threshold_average(
        df, min, max, "net_inflation"
    ),
    "dao_value_capture": lambda df, min, max, frac: threshold_mc_fraction(
        df, min, max, frac, "dao_value_capture"
    ),
    "net_inflation_dao_value_capture_elasticity": lambda df, min, max: threshold_elasticity(
        df, min, max, "net_inflation_dao_value_capture_elasticity"
    ),
    "network_load_balancing": lambda df, min, max, frac: threshold_load_balancing(
        df, min, max, frac, "network_load_balancing"
    ),
}


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
    ]:
        raise ValueError("Error: unsupported threshold inequality type")

    if "ratio" in entity:
        kpi = "ratio"
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

    df["ratio"] = df[kpi[0]] / df[kpi[1]]

    return threshold_average(df, min, max, entity)


def threshold_elasticity(df, min, max, entity):
    if entity not in ["net_inflation_dao_value_capture_elasticity"]:
        raise ValueError("Error: unsupported threshold inequality type")

    kpi = KPI_MAP[entity]

    df_delta = df.pct_change()
    df_delta["elasticity"] = df_delta[kpi[0]] / df_delta[kpi[1]]
    df.drop(df.index[:1], inplace=True)
    df["elasticity"] = df_delta["elasticity"]

    return threshold_average(df, min, max, entity)
