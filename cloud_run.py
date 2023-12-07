from model import run_experiments
import pickle
import sys

experiments = sys.argv[1:]
df = run_experiments(experiments)

file_name = open("data/{}.pkl".format("-".join(experiments)), "ab")
pickle.dump(df, file_name)
file_name.close()
print("Complete!")
