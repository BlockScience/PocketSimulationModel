from model import run_experiments
import pickle

experiment_name = "Base"
df = run_experiments([experiment_name])

file_name = open("data/{}.pkl".format(experiment_name), "ab")
pickle.dump(df, file_name)
file_name.close()
print("Complete!")
