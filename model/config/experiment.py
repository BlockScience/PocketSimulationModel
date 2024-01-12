from typing import List

experimental_setups = {
    "test1": {
        "config_option_state": "Test",
        "config_option_params": "Test",
        "monte_carlo_n": 1,
        "T": 365,
    },
    "Base": {
        "config_option_state": "Base",
        "config_option_params": "Base",
        "monte_carlo_n": 1,
        "T": 365,
    },
    "BaseDynamic": {
        "config_option_state": "Base",
        "config_option_params": "BaseDynamic",
        "monte_carlo_n": 1,
        "T": 365,
    },
}



for i in range(1, 28):
    experimental_setups["Test{}".format(i)] = {
        "config_option_state": "Base",
        "config_option_params": "Test{}".format(i),
        "monte_carlo_n": 1,
        "T": 365,
    }

for i in range(1, 289):
    experimental_setups["gateway_viability_sweep_ag1_{}".format(i)] = {
        "config_option_state": "Base",
        "config_option_params": "gateway_viability_sweep_ag1_{}".format(i),
        "monte_carlo_n": 1,
        "T": 365,
    }

def add_experiments_from_param_strings(param_strings: List[str],
                                      monte_carlo_n: int,
                                      T: int,
                                      experiment_dict = experimental_setups) -> None:
    """
    Given a list of strings corresponding to parameters,
    add an experimental setup for each one. 
    """
    for param_string in param_strings:
        experiment_dict[param_string] = {
            "config_option_state": "Base",
            "config_option_params": param_string, 
            "monte_carlo_n": monte_carlo_n,
            "T": T 
        }
    return None #Used for side effect of adding to experimental_setups. 


