import pandas as pd
import numpy as np

GRID_NUMBERS = {"gateway_viability_sweep_ag1_": 288}


def check_if_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False


def create_expected_runs_dataframe(s3, experiment_name):
    data = [
        [
            "gateway_viability_sweep_ag1_{}".format(x),
            "data/{}.pkl".format("gateway_viability_sweep_ag1_{}".format(x)),
            "data/Simulation-{}.pkl".format("gateway_viability_sweep_ag1_{}".format(x)),
        ]
        for x in range(1, GRID_NUMBERS[experiment_name] + 1)
    ]
    df = pd.DataFrame(data, columns=["Experiment", "Full Simulation File", "KPI File"])

    # Figure out if runs were complete
    a = df["Full Simulation File"].apply(
        lambda x: check_if_exists(s3, "pocketsimulation", x)
    )
    b = df["KPI File"].apply(lambda x: check_if_exists(s3, "pocketsimulation", x))
    df["Complete"] = a & b
    return df


def create_queue_experiments(runs, chunk_size, join_char=","):
    # Filter to non-complete runs
    runs = runs[~runs["Complete"]]
    runs = runs["Experiment"].values

    # Split the runs
    split_size = len(runs) // chunk_size + (len(runs) % chunk_size > 0)
    runs = np.array_split(runs, split_size)

    # Join groups together
    runs = [join_char.join(x) for x in runs]
    return runs
