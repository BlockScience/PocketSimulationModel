from math import isclose
from model.config.params import build_params, create_sweep
from model import run
from model.config import *

from calc import *

def run_experiment_from_sweep_individual(sweep_individual: dict):
    # TODO: Get the data frame to use

def create_new_binary_sweep_individual(df: pd.DataFrame,
                          col_to_rank_by: str, 
                          keys: List[str]):
   """
   Given an individual (defined as a dictionary whose keys are two-element lists),
   we create a new sweep. 
   """
    best_index = df[col_to_rank_by].idmax() # location of best individual
    best_individual = df.loc[best_index] # find best individual
    best__score = df[col_to_rank_by].max() #best value for ranking
    new_sweep_individual = dict{} # create new sweep individual

    # Loop over the defined keys, in each case keeping the 
    # best individual's value as a bound,  and replacing the 
    # other bound with the average of the two bounds. 

    for key in keys:
        bounds = df[key].unique()
        if len(bounds) == 2:
            lb = min(bounds)
            ub = max(bounds)
            mid = 0.5 * (lb + ub)
            if isclose(best_individual[key],lb):
                new_sweep_individual[key] =  [lb, mid]
            elif isclose(best_individual[key], ub):
                new_sweep_individual_key = [mid, ub]
            else:
                raise Error("Something is wrong. Best individual has issues.")
        else:
            raise Error("Passed an individual with a list who didn't have two elements. ")
            
    return new_sweep_individual


def equal_on_keys(ind_1, ind_2, keys_to_use: list[Str]):
    """
    Check to see if two dictionary individuals are the same,
     i.e. if they take the
    same value for all relevant keys.
    """
    return all([isclose(ind_1.get(key),ind_2.get(key)) 
                for key in ind_1.keys()
                if key in keys_to_use])

def iterate_adaptive_grid_psuu(initial_indvidual,
                               max_repeat_individual = 6,
                               max_repeat_threshold_score = 6,
                               max_steps = 100,
                               col_to_use = ""):
    step = 0
    keys_to_use = initial_individual.keys()

    last_best_individual = None
    last_best_threshold_score = None

    times_individual_repeated = 0
    times_threshold_score = 0

    done = False
    while(not(done)): 
        # Get information and convert to info on individuals
        # Find new individual
        # Check if we are done. 
        # If not, continue.
        # IF yes, indicate. 
    






