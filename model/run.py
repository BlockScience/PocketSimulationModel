import pandas as pd
import numpy as np
from model.psub import psub_blocks
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD import configs
from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import Experiment
from copy import deepcopy
from model.config import build_state, build_params, experimental_setups
import os


def load_config(monte_carlo_runs: int, t: int, params, initial_state):
    sim_config = config_sim(
        {
            "N": monte_carlo_runs,  # number of monte carlo runs
            "T": range(t),  # number of timesteps
            "M": params,  # simulation parameters
        }
    )

    exp = Experiment()
    exp.append_configs(
        sim_configs=sim_config,
        initial_state=initial_state,
        partial_state_update_blocks=psub_blocks,
    )
    return exp


def add_config(exp: Experiment, monte_carlo_runs: int, t: int, params, initial_state):
    sim_config = config_sim(
        {
            "N": monte_carlo_runs,  # number of monte carlo runs
            "T": range(t),  # number of timesteps
            "M": params,  # simulation parameters
        }
    )

    exp.append_configs(
        sim_configs=sim_config,
        initial_state=initial_state,
        partial_state_update_blocks=psub_blocks,
    )


def run(exp) -> pd.DataFrame:
    """
    Run simulation
    """
    # execute in local mode
    exec_mode = ExecutionMode()
    local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)

    sim = Executor(exec_context=local_mode_ctx, configs=exp.configs)
    raw_system_events, _, _ = sim.execute()
    df = pd.DataFrame(raw_system_events)
    return df


def compute_KPIs(df: pd.DataFrame):
    pass


def postprocessing(df: pd.DataFrame, compute_kpis=True) -> pd.DataFrame:
    # Get only the last timestep
    df = df.groupby(["simulation", "subset", "run", "timestep"]).last().reset_index()

    df["key"] = df.apply(
        lambda x: "{}-{}-{}".format(x["simulation"], x["subset"], x["run"]), axis=1
    )

    if compute_kpis:
        compute_KPIs(df)

    return df


def run_experiments(experiment_keys):
    meta_data = []

    experimental_setup = experimental_setups[experiment_keys[0]]
    state = build_state(experimental_setup["config_option_state"])
    params = build_params(experimental_setup["config_option_params"])
    exp = load_config(
        experimental_setup["monte_carlo_n"], experimental_setup["T"], params, state
    )
    meta_data.append(
        [
            experiment_keys[0],
            experimental_setup["config_option_state"],
            experimental_setup["config_option_params"],
        ]
    )

    for key in experiment_keys[1:]:
        experimental_setup = experimental_setups[key]
        state = build_state(experimental_setup["config_option_state"])
        params = build_params(experimental_setup["config_option_params"])
        add_config(
            exp,
            experimental_setup["monte_carlo_n"],
            experimental_setup["T"],
            params,
            state,
        )
        meta_data.append(
            [
                key,
                experimental_setup["config_option_state"],
                experimental_setup["config_option_params"],
            ]
        )

    raw = run(exp)
    compute_KPIs(raw)
    df = postprocessing(raw)
    meta_data = pd.DataFrame(
        meta_data, columns=["Experiment Name", "State Set", "Params Set"]
    )
    df = pd.concat([df, df["simulation"].apply(lambda x: meta_data.loc[x])], axis=1)

    return df


def write_to_csv(df, data_folder, over_write=False):
    for key in df["Experiment Name"].unique():
        if not over_write:
            assert "{}.csv".format(key) not in os.listdir(
                "experiment_data/{}".format(data_folder)
            ), "File already present"
        df[df["Experiment Name"] == key].to_csv(
            "experiment_data/{}/{}.csv".format(data_folder, key)
        )


def auto_run_sets(experiment_keys, data_folder, chunk_size):
    current_runs = [
        x.replace(".csv", "")
        for x in os.listdir("experiment_data/{}".format(data_folder))
    ]
    already_run = []
    new_runs = []
    for x in experiment_keys:
        if x in current_runs:
            already_run.append(x)
        else:
            new_runs.append(x)
    if len(already_run) > 0:
        print("The following have already been run:")
        for x in already_run:
            print(x)
        print()

    while len(new_runs) > 0:
        if chunk_size > len(new_runs):
            next_runs = new_runs
            new_runs = []
        else:
            next_runs = new_runs[-chunk_size:]
            new_runs = new_runs[:-chunk_size]

        print("Running the following:")
        for x in next_runs:
            print(x)
        print()

        df = run_experiments(next_runs)
        write_to_csv(df, data_folder)
