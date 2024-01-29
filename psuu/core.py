import pandas as pd
from model.config.params import *
from .scenario_configs import scenario_configs
from math import isclose
from typing import List, Union
from .meta_programming import build_next_param_config_code
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


KPI_MAP = {
    "servicer_npv": "kpi_1",
    "gateway_npv": "kpi_3",
    "circulating_supply": "kpi_4",
    "available_supply": "kpi_5",
    "servicer_slashing_cost": "kpi_8",
    "dao_value_capture": "kpi_10",
    "servicer_jailing_cost": "kpi_11",
    "servicer_capital_costs": "kpi_14",
    "net_inflation": "kpi_D",
    "circulating_supply_available_supply_ratio": ["kpi_4", "kpi_5"],
    "net_inflation_dao_value_capture_elasticity": ["kpi_D", "kpi_10"],
    "network_load_balancing": "kpi_C_recovery",
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
    "network_load_balancing": lambda df, threshold_parameters: threshold_mc_fraction(
        df,
        threshold_parameters["d1"],
        None,
        threshold_parameters["d2"],
        "network_load_balancing",
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
    kpis["kpi_C_recovery"] = kpis["kpi_c_post"] / kpis["kpi_c_pre"]
    return kpis


def threshold_mc_fraction(df, min, max, frac, entity):
    if entity not in [
        "servicer_npv",
        "gateway_npv",
        "dao_value_capture",
        "servicer_slashing_cost",
        "servicer_jailing_cost",
        "network_load_balancing",
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


def select_best_parameter_constellation(df_thresholds, variable_params):
    mx = df_thresholds["Score"].max()
    pc = df_thresholds[df_thresholds["Score"] == mx]
    pc = pc.sample(1).iloc[0]
    pc = pc.name
    out = {}
    assert len(pc) == len(variable_params)
    for x, y in zip(pc, variable_params):
        out[y] = x
    return out


def update_param_grid(
    old_param_grid: Dict[str, List],
    best_individual: Dict[str, Union[float, int]],
    relevant_keys: set = None,
) -> Dict[str, List]:
    """
    Find the directional average of two param_sets for a given set of keys.

    The best_individual_param_set should be a dictionary where the lists are single elements.
    Relevant keys tells which to average over.

    """

    if relevant_keys is None:
        relevant_keys = set(best_individual.keys())

    # Check that Param Grid to merge with has two values per key.
    assert all(
        [len(val) == 2 for key, val in old_param_grid.items() if key in relevant_keys]
    )

    # Create empty param_grid
    new_param_grid = {}

    # Now we go through and replace one of the two
    # associated bounds with the directional average of the list and the best individual's value.

    # TODO: Check if it is worth converting to map structure; leverage numpy performance?

    for key in old_param_grid.keys():
        if key in relevant_keys:
            # Directional average.
            # TODO: Check if it is worth rewriting directional average as external function.
            bounds = old_param_grid.get(key)
            lb = min(bounds)
            ub = max(bounds)
            mid = 0.5 * (lb + ub)
            best_val = best_individual.get(key)
            if isclose(best_val, lb):
                new_param_grid[key] = [lb, mid]
            elif isclose(best_val, ub):
                new_param_grid[key] = [mid, ub]
            else:
                print(lb, best_val, ub)
                raise Exception(
                    "Something is wrong. The best individual does not have its values close to either the prior upper or lower bound."
                )
        else:
            new_param_grid[key] = old_param_grid.get(key)

    return new_param_grid


def psuu_find_next_grid(sweep):
    (
        sweep_family,
        kpis,
        param_config,
        next_name,
        variable_params,
        control_params,
        threshold_inequalities,
        threshold_parameters,
    ) = load_sweep(sweep)

    df_thresholds = compute_threshold_inequalities(
        kpis, variable_params, threshold_parameters, threshold_inequalities
    )
    df_thresholds["Score"] = df_thresholds.astype(int).sum(axis=1)
    best_param_grid = select_best_parameter_constellation(
        df_thresholds, variable_params
    )
    new_param_grid = update_param_grid(param_config, best_param_grid)
    build_next_param_config_code(
        next_name, new_param_grid, variable_params, control_params, param_config
    )
    return new_param_grid


def load_all_kpi_comparison_data():
    kpi_files = [
        x
        for x in os.listdir("simulation_data")
        if x.endswith(".csv") and not x.endswith("_MC.csv")
    ]
    out = {}
    for file in kpi_files:
        name = file.replace(".csv", "")
        (
            sweep_family,
            kpis,
            param_config,
            next_name,
            variable_params,
            control_params,
            threshold_inequalities,
            threshold_parameters,
        ) = load_sweep(name)

        df_thresholds = compute_threshold_inequalities(
            kpis, variable_params, threshold_parameters, threshold_inequalities
        )

        if sweep_family not in out:
            out[sweep_family] = {}
        number = int(name[:-1].replace(sweep_family, ""))
        out[sweep_family][number] = {
            "variable_params": variable_params,
            "control_params": control_params,
            "param_config": param_config,
            "threshold_passing": df_thresholds.mean(),
        }
    return out

def load_scenario_kpi_comparison_data(scenario_sweep_category):
    kpi_files = [
        x
        for x in os.listdir("simulation_data")
        if x.endswith(".csv") and not x.endswith("_MC.csv") and x.startswith(scenario_sweep_category)
    ]
    out = {}
    for file in kpi_files:
        name = file.replace(".csv", "")
        (
            sweep_family,
            kpis,
            param_config,
            next_name,
            variable_params,
            control_params,
            threshold_inequalities,
            threshold_parameters,
        ) = load_sweep(name)

        df_thresholds = compute_threshold_inequalities(
            kpis, variable_params, threshold_parameters, threshold_inequalities
        )

        if sweep_family not in out:
            out[sweep_family] = {}
        number = int(name[:-1].replace(sweep_family, ""))
        out[sweep_family][number] = {
            "variable_params": variable_params,
            "control_params": control_params,
            "param_config": param_config,
            "threshold_passing": df_thresholds.mean(),
        }
    return out

def decision_tree_feature_importance_plot(scenario_sweep_category, adaptive_grid_number):
    name = scenario_sweep_category + str(adaptive_grid_number) + "_"
    (
        sweep_family,
        kpis,
        param_config,
        next_name,
        variable_params,
        control_params,
        threshold_inequalities,
        threshold_parameters,
    ) = load_sweep(name)

    df_thresholds = compute_threshold_inequalities(
        kpis, variable_params, threshold_parameters, threshold_inequalities
    )

    variable_params = [ "param_" + x for x in variable_params ]

    os.chdir("..")
    from cadcad_machine_search.visualizations import param_sensitivity_plot

    for ti in threshold_inequalities:
        param_sensitivity_plot(df_thresholds, variable_params, ti + '_success', ti + ' inequality threshold')


def threshold_comparison_plot(data):
    print("KPIs are referenced as:")
    for i, x in enumerate(data[1]["threshold_passing"].index):
        print("{}: {}".format(x, i + 1))
    variable_params = data[1]["variable_params"]
    rows = max(data.keys())
    columns = 1 + len(variable_params)
    fig, axes = plt.subplots(rows, ncols=columns, figsize=(20, 3.5 * rows))

    for i in range(rows):
        data_i = data[i + 1]
        for j in range(columns):
            ax = axes[i][j]
            if j == columns - 1:
                passing = data_i["threshold_passing"]
                temp = passing.copy()
                temp.index = list(range(1, len(passing) + 1))
                temp.plot(kind="bar", ax=ax)
                ax.set_title("Threshold Passing Percent")
                ax.bar_label(ax.containers[0])
                ax.set_ylim([0, 1.1])
            else:
                param_name = variable_params[j]
                xmin = data[1]["param_config"][param_name][0]
                xmax = data[1]["param_config"][param_name][1]
                if xmin >= 10000:
                    display_xmin = "{:.2e}".format(xmin)
                else:
                    display_xmin = xmin
                if xmax >= 10000:
                    display_xmax = "{:.2e}".format(xmax)
                else:
                    display_xmax = xmax
                rng = xmax - xmin
                ax.set_xlim(xmin - rng * 0.25, xmax + rng * 0.25)
                ax.set_ylim(0, 10)
                y = 5
                height = 1

                x1 = data[i + 1]["param_config"][param_name][0]
                x2 = data[i + 1]["param_config"][param_name][1]

                display_x1 = x1
                display_x2 = x2

                if x1 >= 10000:
                    display_x1 = "{:.2e}".format(x1)
                if x2 >= 10000:
                    display_x2 = "{:.2e}".format(x2)

                ax.hlines(y, xmin, xmax, color="black")
                ax.vlines(xmin, y - 1, y + 1, color="black")
                ax.vlines(xmax, y - 1, y + 1, color="black")
                ax.text(
                    xmin,
                    y - 2.2,
                    display_xmin,
                    horizontalalignment="center",
                    fontsize=14,
                )
                ax.text(
                    xmax,
                    y - 2.2,
                    display_xmax,
                    horizontalalignment="center",
                    fontsize=14,
                )
                ax.set_title(
                    "{} = \n [{}, {}]".format(param_name, display_x1, display_x2)
                )
                ax.add_patch(Rectangle((x1, y - 1), x2 - x1, 2, color="red", alpha=0.3))
                ax.axis("off")

    plt.show()
