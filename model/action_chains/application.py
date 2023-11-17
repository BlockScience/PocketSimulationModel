from ..boundary_actions import (
    application_join_ba,
    gateway_delegation_ba,
    application_leave_ba,
    gateway_undelegation_ba,
    application_stake_ba,
)
from ..policy import (
    application_join_policy,
    gateway_delegation_policy,
    application_leave_policy,
    gateway_undelegation_policy,
    application_stake_policy,
)
from ..mechanisms import (
    add_application,
    add_gateway_delegator,
    update_application_delegate,
    application_undelegate,
    remove_gateway_delegator,
    remove_application,
    modify_application_pokt_holdings,
    modify_application_stake,
)


def application_join_ac(state, params):
    spaces = application_join_ba(state, params)
    if spaces[0]:
        spaces = application_join_policy(state, params, spaces)
    else:
        return
    if spaces[0]:
        add_application(state, params, spaces)
    else:
        return


def gateway_delegation_ac(state, params, application):
    spaces = gateway_delegation_ba(state, params, application)
    if spaces[0]:
        spaces = gateway_delegation_policy(state, params, spaces)
    else:
        return

    if spaces[0]:
        add_gateway_delegator(state, params, (spaces[0],))
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
            remove_gateway_delegator(state, params, (spaces1,))
        if spaces2:
            remove_application(state, params, ({"application": application},))


def gateway_undelegation_ac(state, params, application):
    spaces = gateway_undelegation_ba(state, params, application)
    if spaces[0]:
        spaces = gateway_undelegation_policy(state, params, spaces)
    else:
        return
    if spaces[0]:
        application_undelegate(state, params, spaces)
        remove_gateway_delegator(state, params, spaces)


def application_stake_ac(state, params):
    spaces = application_stake_ba(state, params)
    for spaces_i in spaces:
        spaces_i = application_stake_policy(state, params, spaces_i)
        modify_application_pokt_holdings(state, params, spaces_i[:1])
        modify_application_stake(state, params, spaces_i[1:])
