from ..boundary_actions import (
    application_join_ba,
    portal_delegation_ba,
    application_leave_ba,
    portal_undelegation_ba,
)
from ..policy import (
    application_join_policy,
    portal_delegation_policy,
    application_leave_policy,
)
from ..mechanisms import (
    add_application,
    add_portal_delegator,
    update_application_delegate,
    application_undelegate,
    remove_portal_delegator,
    remove_application,
)


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


def application_leave_ac(state, params):
    spaces = application_leave_ba(state, params)
    spaces = application_leave_policy(state, params, spaces)
    for application in spaces[0]:
        spaces1 = spaces[0][application]
        spaces2 = spaces[1]["applications"][application]
        if spaces1:
            application_undelegate(state, params, (spaces1,))
            remove_portal_delegator(state, params, (spaces1,))
        if spaces2:
            remove_application(state, params, ({"application": application},))


def portal_undelegation_ac(state, params, application):
    spaces = portal_undelegation_ba(state, params, application)
    print(spaces)
