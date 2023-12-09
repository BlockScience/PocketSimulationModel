import os
import boto3

from model import run_experiments
import pickle
import sys

experiments = sys.argv[1:]
df = run_experiments(experiments)


file_name = open("data/{}.pkl".format("-".join(experiments)), "ab")
pickle.dump(df, file_name)
file_name.close()
print("Complete!")
s3 = boto3.resource("s3")
s3.meta.client.upload_file(
    "data/{}.pkl".format("-".join(experiments)),
    "pocketsimulation",
    "data/{}.pkl".format("-".join(experiments)),
)
print("Uploaded!")
