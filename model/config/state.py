from copy import deepcopy

config_option_map = {"Test": {"Geozones": "Test",
                              "Applications": "Test",
                              "DAO": "Test",
                              "Portals": "Test",
                              "Services": "Test",
                              "Servicers": "Test",
                              "Validators": "Test"}}

def build_state(config_option):
    config_option = config_option_map[config_option]
    state = {}

    state = deepcopy(state)
    return state