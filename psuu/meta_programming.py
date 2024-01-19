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
