import pandas as pd
import numpy as np
from time import sleep
import time
import boto3
from psuu import psuu_find_next_grid, build_next_param_config_code_multi

GRID_NUMBERS = {
    "gateway_viability_sweep_ag1_": 288,
    "network_failures_service_ag1_": 48,
    "servicer_viability_ag1_": 1152,
    "network_viability_ag1_": 3456,
    "network_failures_oracle_ag1_": 3072,
    "gateway_viability_sweep_ag2_": 288,
    "gateway_viability_sweep_ag3_": 288,
    "gateway_viability_sweep_ag4_": 288,
    "gateway_viability_sweep_ag5_": 288,
    "gateway_viability_sweep_ag6_": 288,
    "servicer_viability_ag2_": 1152,
    "servicer_viability_ag3_": 1152,
    "servicer_viability_ag4_": 1152,
    "servicer_viability_ag5_": 1152,
    "servicer_viability_ag6_": 1152,
    "network_failures_service_ag2_": 48,
    "network_viability_ag2_": 3456,
    "servicer_viability_ag3_": 1152,
    "servicer_viability_ag4_": 1152,
    "servicer_viability_ag5_": 1152,
    "servicer_viability_ag6_": 1152,
    "network_failures_service_ag3_": 48,
    "network_viability_ag3_": 3456,
    "network_failures_service_ag4_": 48,
    "network_viability_ag4_": 3456,
    "network_failures_service_ag5_": 48,
    "network_viability_ag5_": 3456,
    "network_failures_service_ag6_": 48,
    "network_viability_ag6_": 3456,
    "network_failures_oracle_ag2_": 3072,
    "network_failures_oracle_ag3_": 3072,
    "network_failures_oracle_ag4_": 3072,
    "network_failures_oracle_ag5_": 3072,
    "network_failures_oracle_ag6_": 3072,
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


def create_expected_runs_dataframe_multi(s3, experiments, run_all=False):
    l = []
    for experiment in experiments:
        l.append(create_expected_runs_dataframe(s3, experiment, run_all=run_all))
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


def download_experiment_mc(experiment, s3, top=None, random=False):
    runs = create_expected_runs_dataframe(s3, experiment, top=top, random=random)
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
        live = ecs.list_tasks(cluster="PocketRuns")["taskArns"]
        if len(live) == max_containers:
            time.sleep(15)
        else:
            q = list(queue.pop(0))
            print(q)
            run_tasks(ecs, list(q))
    live = ecs.list_tasks(cluster="PocketRuns")["taskArns"]
    while len(live) > 0:
        time.sleep(60)
        live = ecs.list_tasks(cluster="PocketRuns")["taskArns"]


def full_run_adaptive_grid(
    grid_names, run_all=False, skip_running=False, skip_download=False
):
    start = time.time()
    session = boto3.Session(profile_name="default")
    s3 = session.client("s3")
    ecs = boto3.client("ecs")
    if not skip_running:
        print("-----Creating Expected Runs Dataframe-----")
        runs = create_expected_runs_dataframe_multi(s3, grid_names, run_all=run_all)
        print("-----Launching Containers-----")
        queue_and_launch(runs, ecs, 20, 20)
        print("-----Downloading KPIs-----")
    if not skip_download:
        for name in grid_names:
            download_experiment_kpi(name, s3)
    print("-----Determining Next Grids-----")
    l = []
    for name in grid_names:
        print()
        print(name)
        print()
        l.append(psuu_find_next_grid(name))
    build_next_param_config_code_multi(
        [x[0] for x in l],
        [x[1] for x in l],
        [x[2] for x in l],
        [x[3] for x in l],
        [x[4] for x in l],
    )

    end = time.time()
    print()
    print("Runs took {} hours.".format((end - start) / 60 / 60))
