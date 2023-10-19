from ..boundary_actions import service_join_ba
from ..policy import service_join_policy
from ..mechanisms import add_service


def service_join_ac(state, params):
    spaces = service_join_ba(state, params)
    if spaces[0]:
        spaces = service_join_policy(state, params, spaces)
    else:
        return
    add_service(state, params, spaces)
