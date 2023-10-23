from ..boundary_actions import (
    servicer_join_ba,
    relay_requests_ba,
    submit_relay_requests_ba,
)
from ..policy import (
    servicer_join_policy,
    submit_relay_requests_policy,
    servicer_relay_policy,
)
from ..mechanisms import (
    add_servicer,
    create_new_session,
    modify_portal_stake,
    modify_application_stake,
    increase_relay_fees,
)
from ..spaces import modify_portal_pokt_space


def servicer_join_ac(state, params):
    spaces = servicer_join_ba(state, params)
    if spaces[0]:
        spaces = servicer_join_policy(state, params, spaces)
    else:
        return
    add_servicer(state, params, spaces)


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
    if type(spaces[0]) == modify_portal_pokt_space:
        modify_portal_stake(state, params, spaces[:1])
    else:
        modify_application_stake(state, params, spaces[:1])
    # spaces2 = burn_per_relay_policy(state, params, spaces[1:2])
    # burn_pokt_mechanism(state, params, spaces2[:1])
    # modify_application_stake(state, params, spaces2[1:])
    increase_relay_fees(state, params, spaces[2:3])
