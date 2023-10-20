from ..boundary_actions import application_join_ba
from ..policy import application_join_policy
from ..mechanisms import add_application


def application_join_ac(state, params):
    spaces = application_join_ba(state, params)
    if spaces[0]:
        spaces = application_join_policy(state, params, spaces)
    else:
        return
    add_application(state, params, spaces)
