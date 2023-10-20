from ..boundary_actions import portal_join_ba
from ..policy import portal_join_policy
from ..mechanisms import add_portal


def portal_join_ac(state, params):
    spaces = portal_join_ba(state, params)
    if spaces[0]:
        spaces = portal_join_policy(state, params, spaces)
    else:
        return
    add_portal(state, params, spaces)
