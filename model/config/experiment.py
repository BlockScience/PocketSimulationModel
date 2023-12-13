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
}

for i in range(1, 5):
    experimental_setups["Test{}".format(i)] = {
        "config_option_state": "Base",
        "config_option_params": "Test{}".format(i),
        "monte_carlo_n": 1,
        "T": 365,
    }
