from copy import deepcopy

config_option_map = {"Test": {"System": "Test",
                              "Behaviors": "Test"}}

def build_params(config_option):
    config_option = config_option_map[config_option]
    a = system_param_config[config_option["System"]]
    b = behavior_param_config[config_option["Behaviors"]]
    params = {**a, **b}

    params = deepcopy(params)
    return params

system_param_config = {"Test": {"A": 1}}

behavior_param_config = {"Test": {"B": 1}}