from ..boundary_actions import (
    service_join_ba,
    service_linking_ba,
    service_leave_ba,
    service_unlinking_ba,
)
from ..policy import (
    service_join_policy,
    service_linking_policy,
    service_leave_policy,
    service_unlinking_policy,
)
from ..mechanisms import (
    add_service,
    link_service_mechanism,
    unlink_service_mechanism,
    remove_service,
)


def service_join_ac(state, params):
    spaces = service_join_ba(state, params)
    if spaces[0]:
        spaces = service_join_policy(state, params, spaces)
    else:
        return
    add_service(state, params, spaces)


def service_linking_ac(state, params, servicer):
    spaces = service_linking_ba(state, params, servicer)
    for space in spaces:
        spaces_i = service_linking_policy(state, params, space)
        if spaces_i[0]:
            link_service_mechanism(state, params, spaces_i)


def service_leave_ac(state, params):
    spaces = service_leave_ba(state, params)
    spaces = service_leave_policy(state, params, spaces)
    for spaces_i in spaces[0]:
        unlink_service_mechanism(state, params, spaces_i)
    for spaces_i in spaces[1]:
        remove_service(state, params, spaces_i)


def service_unlinking_ac(state, params, servicer):
    spaces = service_unlinking_ba(state, params, servicer)
    for space in spaces:
        spaces_i = service_unlinking_policy(state, params, space)
        if spaces_i[0]:
            unlink_service_mechanism(state, params, spaces_i)
