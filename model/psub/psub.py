from .meta import p_update_time, s_update_height, s_update_day
from .servicer import (
    p_servicers_join,
    s_update_servicers,
    p_relay_requests,
    p_jailing_slashing,
    p_servicers_leave,
    p_servicers_stake,
)
from .service import (
    p_service_linking,
    s_update_services,
    p_service_join,
    p_service_unlinking,
    p_service_leave,
)
from .gateway import p_gateway_join, s_update_gateways, p_gateway_leave, p_gateway_stake
from .application import (
    p_application_join,
    s_update_applications,
    p_gateway_delegation,
    p_gateway_undelegation,
    p_application_leave,
    p_application_stake,
)
from .treasury import (
    p_block_reward,
    p_fee_reward,
    s_update_treasury,
    s_update_total_relays,
    s_update_processed_relays,
    p_update_price,
    s_update_pokt_price_true,
    s_update_pokt_price_oracle,
)
from .validator import s_update_validators


# Block for recording things like time
meta_update_block = {
    "policies": {"t": p_update_time, "price": p_update_price},
    "variables": {
        "day": s_update_day,
        "height": s_update_height,
        "pokt_price_true": s_update_pokt_price_true,
        "pokt_price_oracle": s_update_pokt_price_oracle,
    },
}


# Block for anything joining the system
join_block = {
    "policies": {
        "servicer": p_servicers_join,
        "service": p_service_join,
        "gateway": p_gateway_join,
        "application": p_application_join,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Gateways": s_update_gateways,
        "Applications": s_update_applications,
    },
}

# Block for any staking
stake_block = {
    "policies": {
        "servicer": p_servicers_stake,
        "application": p_application_stake,
        "gateway": p_gateway_stake,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Applications": s_update_applications,
        "Gateways": s_update_gateways,
    },
}

# Gateway delegation and service linking
delegation_service_block = {
    "policies": {
        "service_link": p_service_linking,
        "gateway_delegation": p_gateway_delegation,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Gateways": s_update_gateways,
        "Applications": s_update_applications,
    },
}

# Relay requests
relay_requests_block = {
    "policies": {"relay_requests": p_relay_requests},
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Gateways": s_update_gateways,
        "Applications": s_update_applications,
        "total_relays": s_update_total_relays,
        "processed_relays": s_update_processed_relays,
    },
}

# Block for jailing or slashing behaviors
jailing_slashing_block = {
    "policies": {"jailing_slashing": p_jailing_slashing},
    "variables": {
        "Servicers": s_update_servicers,
        "Gateways": s_update_gateways,
    },
}

# Reward disbursement
block_and_fee_rewards_block = {
    "policies": {"block_reward": p_block_reward, "fee_reward": p_fee_reward},
    "variables": {
        "Treasury": s_update_treasury,
        "Validators": s_update_validators,
        "Servicers": s_update_servicers,
        "Gateways": s_update_gateways,
        "Applications": s_update_applications,
    },
}

# Undelegation and service unlinking block
undelegation_unservice_block = {
    "policies": {
        "service_unlink": p_service_unlinking,
        "gateway_undelegation": p_gateway_undelegation,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Gateways": s_update_gateways,
        "Applications": s_update_applications,
    },
}

# Any entities leaving the system
leave_block = {
    "policies": {
        "servicer": p_servicers_leave,
        "service": p_service_leave,
        "gateway": p_gateway_leave,
        "application": p_application_leave,
    },
    "variables": {
        "Servicers": s_update_servicers,
        "Services": s_update_services,
        "Gateways": s_update_gateways,
        "Applications": s_update_applications,
    },
}


psub_blocks = [
    meta_update_block,
    join_block,
    stake_block,
    delegation_service_block,
    relay_requests_block,
    jailing_slashing_block,
    block_and_fee_rewards_block,
    undelegation_unservice_block,
    leave_block,
]
