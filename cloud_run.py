import os
import boto3

from model import run_experiments
import pickle
import sys
from datetime import datetime

print(datetime.now())

experiments = sys.argv[1:]
df, simulation_kpis = run_experiments(experiments)


file_name = open("data/{}.pkl".format("-".join(experiments)), "ab")
pickle.dump(df, file_name)
file_name.close()

file_name = open("data/Simulation-{}.pkl".format("-".join(experiments)), "ab")
pickle.dump(simulation_kpis, file_name)
file_name.close()

print("Complete!")

session = boto3.Session(profile_name="sean")
s3 = session.client("s3")
s3.upload_file(
    "data/{}.pkl".format("-".join(experiments)),
    "pocketsimulation",
    "data/{}.pkl".format("-".join(experiments)),
)
s3.upload_file(
    "data/Simulation-{}.pkl".format("-".join(experiments)),
    "pocketsimulation",
    "data/Simulation-{}.pkl".format("-".join(experiments)),
)
print("Uploaded!")
print(datetime.now())
