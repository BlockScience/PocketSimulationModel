from ..boundary_actions import application_join_ba


def application_join_ac(state, params):
    spaces = application_join_ba(state, params)
    print(spaces)
