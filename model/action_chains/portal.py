from ..boundary_actions import portal_join_ba, portal_leave_ba
from ..policy import portal_join_policy, portal_leave_policy
from ..mechanisms import (
    add_portal,
    application_undelegate,
    remove_portal_delegator,
    remove_portal,
)
from ..spaces import application_undelegation_space


def portal_join_ac(state, params):
    spaces = portal_join_ba(state, params)
    if spaces[0]:
        spaces = portal_join_policy(state, params, spaces)
    else:
        return
    add_portal(state, params, spaces)


def portal_leave_ac(state, params):
    spaces = portal_leave_ba(state, params)
    spaces = portal_leave_policy(state, params, spaces)
    for portal in spaces[0]["portals"]:
        if spaces[0]["portals"][portal]:
            for application in portal.delegators:
                spaces1: application_undelegation_space = {
                    "application_public_key": application,
                    "portal_public_key": portal,
                }
                application_undelegate(state, params, (spaces1,))
                remove_portal_delegator(state, params, (spaces1,))
            remove_portal(state, params, ({"portal": portal},))
