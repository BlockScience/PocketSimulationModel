import pandas as pd
import numpy as np
from time import sleep
import time

GRID_NUMBERS = {
    "gateway_viability_sweep_ag1_": 288,
    "network_failures_service_ag1_": 48,
    "servicer_viability_ag1_": 1152,
    "network_viability_ag1_": 1152,
    "network_failures_oracle_ag1_": 2688,
    "gateway_viability_sweep_ag2_": 288,
    "gateway_viability_sweep_ag3_": 288,
    "gateway_viability_sweep_ag4_": 288,
}


def check_if_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False


def create_expected_runs_dataframe(
    s3, experiment_name, run_all=False, top=None, random=False
):
    data = [
        [
            "{}{}".format(experiment_name, x),
            "data/{}.pkl".format("{}{}".format(experiment_name, x)),
            "data/Simulation-{}.pkl".format("{}{}".format(experiment_name, x)),
        ]
        for x in range(1, GRID_NUMBERS[experiment_name] + 1)
    ]
    df = pd.DataFrame(data, columns=["Experiment", "Full Simulation File", "KPI File"])
    if top:
        if random:
            df = df.sample(top)
        else:
            df = df.iloc[:top]

    # Figure out if runs were complete
    if run_all:
        df["Complete"] = False
    else:
        a = df["Full Simulation File"].apply(
            lambda x: check_if_exists(s3, "pocketsimulation", x)
        )
        b = df["KPI File"].apply(lambda x: check_if_exists(s3, "pocketsimulation", x))
        df["Complete"] = a & b
    return df


def create_expected_runs_dataframe_multi(s3, experiments):
    l = []
    for experiment in experiments:
        l.append(create_expected_runs_dataframe(s3, experiment))
        l[-1]["Group"] = experiment
    df = pd.concat(l)
    return df


def create_queue_experiments(runs, chunk_size, join_char=","):
    # Filter to non-complete runs
    runs = runs[~runs["Complete"]]
    runs = runs["Experiment"].values

    # Split the runs
    split_size = len(runs) // chunk_size + (len(runs) % chunk_size > 0)
    runs = np.array_split(runs, split_size)

    # Join groups together
    # runs = [join_char.join(x) for x in runs]

    return runs


def run_tasks(ecs, experiments):
    print(
        ecs.run_task(
            cluster="PocketRuns",
            count=1,
            launchType="FARGATE",
            overrides={
                "containerOverrides": [
                    {
                        "name": "pocket",
                        "command": experiments,
                    },
                ],
            },
            taskDefinition="Simulation-Run",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": [
                        "subnet-03584b39cf34b8789",
                        "subnet-0e214e434065774f3",
                        "subnet-09452d6bdd5634c80",
                    ],
                    "securityGroups": [
                        "sg-0da6cc582b0e773c5",
                    ],
                    "assignPublicIp": "ENABLED",
                }
            },
        )["failures"]
    )


def download_experiment_kpi(experiment, s3):
    runs = create_expected_runs_dataframe(s3, experiment)
    assert runs["Complete"].all()

    files = []
    for file in runs["KPI File"]:
        file2 = file.replace("data", "simulation_data")
        files.append(file2)
        with open(file2, "wb") as f:
            s3.download_fileobj("pocketsimulation", file, f)

    dataframes = []
    for file in files:
        dataframes.append(pd.read_pickle(file))
    df = pd.concat(dataframes)
    df = df.reset_index(drop=True)
    df.to_csv("simulation_data/{}.csv".format(experiment))


def download_experiment_mc(experiment, s3, top=None):
    runs = create_expected_runs_dataframe(s3, experiment, top=top)
    assert runs["Complete"].all()

    files = []
    for file in runs["Full Simulation File"]:
        file2 = file.replace("data", "simulation_data")
        files.append(file2)
        with open(file2, "wb") as f:
            s3.download_fileobj("pocketsimulation", file, f)

    dataframes = []
    for file in files:
        dataframes.append(pd.read_pickle(file))
    df = pd.concat(dataframes)
    df = df.reset_index(drop=True)
    df.to_csv("simulation_data/{}MC.csv".format(experiment))


def queue_and_launch(runs, ecs, n, sleep_minutes, max_containers=12):
    queue = create_queue_experiments(runs, n)
    while len(queue) > 0:
        for _ in range(max_containers):
            if len(queue) > 0:
                q = list(queue.pop(0))
                print(q)
                run_tasks(ecs, list(q))
        print()
        print()
        time.sleep(sleep_minutes * 60)
