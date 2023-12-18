import pandas as pd

GRID_NUMBERS = {"gateway_viability_sweep_ag1_": 288}


def create_expected_runs_dataframe(experiment_name):
    data = [
        [
            "gateway_viability_sweep_ag1_{}".format(x),
            "data/{}.pkl".format(x),
            "data/Simulation-{}.pkl".format(x),
        ]
        for x in range(1, GRID_NUMBERS[experiment_name] + 1)
    ]
    df = pd.DataFrame(data, columns=["Experiment", "Full Simulation File", "KPI File"])
    return df
