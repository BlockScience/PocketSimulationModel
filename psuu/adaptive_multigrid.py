from itertools import product
from math import isclose

import numpy as np
import pandas as pd
from random import choice
from typing import Callable, Dict, List, Union

from model.run import run_experiments
from model.config.params import *
from model.config.experiment import *

###########################################
## Methods for creating name strings     ##
#
replacement_dict = {
    "session_token_bucket_coefficient": "stbc",
    "gateway_fee_per_relay": "gfpr",
    "application_fee_per_relay": "afpr",
    "gateway_minimum_stake": "gms",
    "minimum_application_stake": "ams",
    "param_session_token_bucket_coefficient": "stbc",
    "param_gateway_fee_per_relay": "gfpr",
    "param_application_fee_per_relay": "afpr",
    "param_gateway_minimum_stake": "gms",
    "param_minimum_application_stake": "ams",
}

name_map = lambda x: "_".join(
    f"{replacement_dict.get(key, key)}:{val}" for key, val in x.items()
)


def add_experiments_from_param_strings(
    param_strings: List[str],
    monte_carlo_n: int,
    T: int,
    experiment_dict=experimental_setups,
) -> None:
    """
    Given a list of strings corresponding to parameters,
    add an experimental setup for each one.
    """
    for param_string in param_strings:
        experiment_dict[param_string] = {
            "config_option_state": "Base",
            "config_option_params": param_string,
            "monte_carlo_n": monte_carlo_n,
            "T": T,
        }
    return None  # Used for side effect of adding to experimental_setups.


def build_individual_dict_from_param_grid(
    param_grid: Dict[str, List], name_map_to_use: Callable[str, str] = name_map
):
    print("Building the individual dict.")
    list_of_value_combinations = list(product(*param_grid.values()))
    my_list = [dict(zip(param_grid.keys(), v)) for v in list_of_value_combinations]
    individual_dict = {name_map(my_list[k]): my_list[k] for k in range(len(my_list))}
    print(f"Individual dict is {individual_dict}")
    return individual_dict


def update_param_grid(
    old_param_grid: Dict[str, List],
    best_individual: Dict[str, Union[float, int]],
    relevant_keys: set = None,
) -> Dict[str, List]:
    """
    Find the directional average of two param_sets for a given set of keys.

    The best_individual_param_set should be a dictionary where the lists are single elements.
    Relevant keys tells which to average over.

    """

    if relevant_keys is None:
        relevant_keys = set(best_individual.keys())

    # Check that Param Grid to merge with has two values per key.
    assert all(
        [len(val) == 2 for key, val in old_param_grid.items() if key in relevant_keys]
    )

    # Create empty param_grid
    new_param_grid = {}

    # Now we go through and replace one of the two
    # associated bounds with the directional average of the list and the best individual's value.

    # TODO: Check if it is worth converting to map structure; leverage numpy performance?

    for key in old_param_grid.keys():
        if key in relevant_keys:
            # Directional average.
            # TODO: Check if it is worth rewriting directional average as external function.
            bounds = old_param_grid.get(key)
            lb = min(bounds)
            ub = max(bounds)
            mid = 0.5 * (lb + ub)
            best_val = best_individual.get(key)
            if isclose(best_val, lb):
                new_param_grid[key] = [lb, mid]
            elif isclose(best_val, ub):
                new_param_grid[key] = [mid, ub]
            else:
                raise Exception(
                    "Something is wrong. The best individual does not have its values close to either the prior upper or lower bound."
                )
        else:
            new_param_grid[key] = old_param_grid.get(key)

    return new_param_grid


def iterate_adaptive_multigrid(
    initial_param_grid: Dict[str, List],
    other_params_to_sweep: Dict[str, List],
    prefix: str,
    max_repeat_best_name: int = 6,
    max_repeat_best_fitness: int = 6,
    max_steps: int = 100,
    fitness_func: Callable[pd.Series, float] = None,
) -> dict:
    """
    Perform directed search in the space of param_grids, as defined by initial_param_grid.
    """

    ############################
    ## Basic Setup: Deciding  ##
    ## which keys to use, and ##
    ## setting up steps.      ##
    ############################

    step = 0

    new_param_grid = deepcopy(initial_param_grid)

    new_best_name = ""
    new_best_fitness = -np.inf

    times_repeat_best_name = 0
    times_repeat_best_fitness = 0

    finished = False

    while not (finished):
        old_param_grid = deepcopy(new_param_grid)
        old_best_name = new_best_name
        old_best_fitness = new_best_fitness

        individual_dict = build_individual_dict_from_param_grid(old_param_grid)
        print(individual_dict)

        # TODO: update from mock to actual.
        data = get_data_from_param_grid(
            param_grid=new_param_grid,
            other_params_to_sweep=other_params_to_sweep,
            prefix=prefix,
        )
        data = give_data_individual_names(data)

        new_best_name, new_best_val = find_best_individual_name(
            data, fitness_func=fitness_func, name_biased_towards=old_best_name
        )

        assert not (
            new_best_name is None
        ), "The best individual should be somewhere in this dictionary."
        print(new_best_name)

        new_best_individual = individual_dict[new_best_name]

        if new_best_name == old_best_name:
            times_repeat_best_name = times_repeat_best_name + 1
        else:
            times_repeat_best_name = 0

        if isclose(new_best_fitness, old_best_fitness):
            times_repeat_best_fitness = times_repeat_best_fitness + 1
        else:
            times_repeat_best_fitness = 0

        step = step + 1
        print(f"Starting step {step}.")

        finished_condition_1 = step > max_steps
        finished_condition_2 = times_repeat_best_name > max_repeat_best_name
        finished_condition_3 = times_repeat_best_fitness > max_repeat_best_fitness

        finished = finished_condition_1 or finished_condition_2 or finished_condition_3

        if not (finished):
            new_param_grid = update_param_grid(
                old_param_grid=old_param_grid, best_individual=new_best_individual
            )

        # Absorb data into a useful dictionary for analysis, after while loop is terminated.
    info_dict = {}
    info_dict["final_best_individual"] = new_best_individual
    info_dict["final_param_grid"] = new_param_grid
    info_dict["final_best_fitness"] = new_best_val
    info_dict["final_data_frame"] = data
    info_dict["final_step"] = step
    info_dict["final_fitness_repeat_count"] = times_repeat_best_fitness
    info_dict["final_best_individual_repeat"] = times_repeat_best_name

    return info_dict
