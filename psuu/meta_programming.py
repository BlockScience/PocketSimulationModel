def build_next_param_config_code(
    next_name, new_param_grid, control_params, param_config
):
    print("Add the following to model/config/params.py:")
    print()
    print('{} = build_params("Base")'.format(next_name))
    for x in new_param_grid:
        print('{}["{}"] = {}'.format(next_name, x, new_param_grid[x]))
    for x in control_params:
        print('{}["{}"] = {}'.format(next_name, x, param_config[x]))
    print('create_sweep("{}",{},config_option_map_sweep)'.format(next_name, next_name))
    print()
    print()
    combos = 1
    for x in new_param_grid.values():
        combos = combos * len(x)
    for x in control_params:
        combos = combos * len(param_config[x])
    print("Add the following to model/config/experiment.py:")
    print()
    print(
        """for i in range(1, {}):
    experimental_setups["{}{{}}".format(i)] = {{
        "config_option_state": "Base",
        "config_option_params": "{}{{}}".format(i),
        "monte_carlo_n": 5,
        "T": 365,
    }}""".format(
            combos + 1, next_name, next_name
        )
    )
    print()
    print()
    print("Add the following to GRID_NUMBERS in cloud_utility.py")
    print('"{}": {}'.format(next_name, combos))
