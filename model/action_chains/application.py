from ..boundary_actions import application_join_ba, portal_delegation_ba
from ..policy import application_join_policy, portal_delegation_policy
from ..mechanisms import add_application, add_portal_delegator, update_application_delegate


def application_join_ac(state, params):
    spaces = application_join_ba(state, params)
    if spaces[0]:
        spaces = application_join_policy(state, params, spaces)
    else:
        return
    add_application(state, params, spaces)

def portal_delegation_ac(state, params, application):
    spaces = portal_delegation_ba(state, params, application)
    if spaces[0]:
        spaces = portal_delegation_policy(state, params, spaces)
    else:
        return

    if spaces[0]:
        add_portal_delegator(state, params, (spaces[0],))
        update_application_delegate(state, params, (spaces[1],))
    else:
        return
