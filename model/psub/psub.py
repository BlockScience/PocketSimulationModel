from .meta import p_update_time, s_update_height, s_update_day
from .servicer import (
    p_servicers_join,
    s_update_servicers,
    p_relay_requests,
    p_jailing_slashing,
    p_servicers_leave,
)
from .service import (
    p_service_linking,
    s_update_services,
    p_service_join,
    p_service_unlinking,
    p_service_leave,
)
from .portal import p_portal_join, s_update_portals, p_portal_leave
from .application import (
    p_application_join,
    s_update_applications,
    p_portal_delegation,
    p_portal_undelegation,
    p_application_leave,
)
from .treasury import p_block_reward, p_fee_reward, s_update_treasury
from .validator import s_update_validators

# Block for recording things like time
meta_update_block = {
    "policies": {
        "t": p_update_time,
    },
    "variables": {"day": s_update_day, "height": s_update_height},
}

# Block for anything joining the system
join_block = {
    "policies": {
        "servicer": p_servicers_join,
        "service": p_service_join,
        "portal": p_portal_join,
        "application": p_application_join,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Portals": s_update_portals,
        "Applications": s_update_applications,
    },
}

# Portal delegation and service linking
delegation_service_block = {
    "policies": {
        "service_link": p_service_linking,
        "portal_delegation": p_portal_delegation,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Portals": s_update_portals,
        "Applications": s_update_applications,
    },
}

# Relay requests
relay_requests_block = {
    "policies": {"relay_requests": p_relay_requests},
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Portals": s_update_portals,
        "Applications": s_update_applications,
    },
}

# Block for jailing or slashing behaviors
jailing_slashing_block = {
    "policies": {"jailing_slashing": p_jailing_slashing},
    "variables": {
        "Services": s_update_services,
        "Portals": s_update_portals,
    },
}

# Reward disbursement
block_and_fee_rewards_block = {
    "policies": {"block_reward": p_block_reward, "fee_reward": p_fee_reward},
    "variables": {
        "Treasury": s_update_treasury,
        "Validators": s_update_validators,
        "Servicers": s_update_servicers,
        "Portals": s_update_portals,
        "Applications": s_update_applications,
    },
}

# Undelegation and service unlinking block
undelegation_unservice_block = {
    "policies": {
        "service_unlink": p_service_unlinking,
        "portal_undelegation": p_portal_undelegation,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Portals": s_update_portals,
        "Applications": s_update_applications,
    },
}

# Any entities leaving the system
leave_block = {
    "policies": {
        "servicer": p_servicers_leave,
        "service": p_service_leave,
        "portal": p_portal_leave,
        "application": p_application_leave,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Portals": s_update_portals,
        "Applications": s_update_applications,
    },
}


psub_blocks = [
    meta_update_block,
    join_block,
    delegation_service_block,
    relay_requests_block,
    jailing_slashing_block,
    block_and_fee_rewards_block,
    undelegation_unservice_block,
    leave_block,
]
