from ..boundary_actions import (
    servicer_join_ba,
    relay_requests_ba,
    submit_relay_requests_ba,
    servicer_leave_ba,
    servicer_stake_ba,
)
from ..policy import (
    servicer_join_policy,
    submit_relay_requests_policy,
    servicer_relay_policy,
    servicer_leave_policy,
    servicer_stake_policy,
)
from ..mechanisms import (
    add_servicer,
    create_new_session,
    modify_gateway_stake,
    modify_application_stake,
    increase_relay_fees,
    modify_servicer_pokt_holdings,
    remove_session,
    unlink_service_mechanism,
    remove_servicer,
    modify_servicer_stake,
)
from ..spaces import modify_gateway_pokt_space


def servicer_join_ac(state, params):
    spaces = servicer_join_ba(state, params)
    if spaces[0]:
        spaces = servicer_join_policy(state, params, spaces)
    else:
        return
    if spaces[0]:
        add_servicer(state, params, spaces)
    else:
        return


def relay_requests_ac(state, params):
    # Submit request
    spaces = submit_relay_requests_ba(state, params)
    spaces = submit_relay_requests_policy(state, params, spaces)

    create_new_session(state, params, spaces[:1])

    # spaces = burn_per_session_policy(state, params, spaces)
    # burn_pokt_mechanism(state, params, spaces[:1])
    # modify_application_stake(state, params, spaces[1:])

    # Relay the request
    spaces = relay_requests_ba(state, params)
    spaces = servicer_relay_policy(state, params, spaces)
    if type(spaces[0]) == modify_gateway_pokt_space:
        modify_gateway_stake(state, params, spaces[:1])
    else:
        modify_application_stake(state, params, spaces[:1])
    # spaces2 = burn_per_relay_policy(state, params, spaces[1:2])
    # burn_pokt_mechanism(state, params, spaces2[:1])
    # modify_application_stake(state, params, spaces2[1:])
    increase_relay_fees(state, params, spaces[2:3])
    if spaces[3]:
        remove_session(state, params, spaces[3:4])


def servicer_leave_ac(state, params):
    spaces = servicer_leave_ba(state, params)
    spaces = servicer_leave_policy(state, params, spaces)

    for spaces_i in spaces[0]:
        unlink_service_mechanism(state, params, spaces_i)
    for spaces_i in spaces[1]:
        remove_servicer(state, params, spaces_i)


def servicers_stake_ac(state, params):
    spaces = servicer_stake_ba(state, params)
    for spaces_i in spaces:
        spaces_i = servicer_stake_policy(state, params, spaces_i)
        modify_servicer_pokt_holdings(state, params, spaces_i[:1])
        modify_servicer_stake(state, params, spaces_i[1:])
