import os
import boto3

from model import run_experiments
import pickle
import sys
from datetime import datetime
from cadCAD.engine import ExecutionMode

print(datetime.now())

experiments = sys.argv[1:]
df, simulation_kpis = run_experiments(experiments, context=ExecutionMode().local_mode)

for key in df["Experiment Name"].unique():
    file_name = open("data/{}.pkl".format(key), "ab")
    pickle.dump(df[df["Experiment Name"] == key], file_name)
    file_name.close()

    file_name = open("data/Simulation-{}.pkl".format(key), "ab")
    pickle.dump(simulation_kpis[simulation_kpis["Experiment Name"] == key], file_name)
    file_name.close()

print("Complete!")

session = boto3.Session(profile_name="sean")
s3 = session.client("s3")
for key in df["Experiment Name"].unique():
    s3.upload_file(
        "data/{}.pkl".format(key),
        "pocketsimulation",
        "data/{}.pkl".format(key),
    )
    s3.upload_file(
        "data/Simulation-{}.pkl".format(key),
        "pocketsimulation",
        "data/Simulation-{}.pkl".format(key),
    )
print("Uploaded!")
print(datetime.now())
