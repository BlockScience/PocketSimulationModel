from ..boundary_actions import gateway_join_ba, gateway_leave_ba
from ..policy import gateway_join_policy, gateway_leave_policy
from ..mechanisms import (
    add_gateway,
    application_undelegate,
    remove_gateway_delegator,
    remove_gateway,
)
from ..spaces import application_undelegation_space


def gateway_join_ac(state, params):
    spaces = gateway_join_ba(state, params)
    if spaces[0]:
        spaces = gateway_join_policy(state, params, spaces)
    else:
        return
    if spaces[0]:
        add_gateway(state, params, spaces)
    else:
        pass


def gateway_leave_ac(state, params):
    spaces = gateway_leave_ba(state, params)
    spaces = gateway_leave_policy(state, params, spaces)
    for gateway in spaces[0]["gateways"]:
        if spaces[0]["gateways"][gateway]:
            for application in gateway.delegators:
                spaces1: application_undelegation_space = {
                    "application_public_key": application,
                    "gateway_public_key": gateway,
                }
                application_undelegate(state, params, (spaces1,))
                remove_gateway_delegator(state, params, (spaces1,))
            remove_gateway(state, params, ({"gateway": gateway},))
