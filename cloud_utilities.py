import pandas as pd
import numpy as np

GRID_NUMBERS = {
    "gateway_viability_sweep_ag1_": 288,
    "network_failures_service_ag1_": 48,
    "servicer_viability_ag1": 1152,
}


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
    # runs = [join_char.join(x) for x in runs]

    return runs


def run_tasks(ecs, experiments):
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
