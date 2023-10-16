from .meta import p_update_time, s_update_height, s_update_day

# Block for recording things like time
meta_update_block = {
    "policies": {
        "t": p_update_time,
    },
    "variables": {"day": s_update_day, "height": s_update_height},
}

# Block for anything joining the system
join_block = {"policies": {}, "variables": {}}

# Portal delegation and service linking
delegation_service_block = {"policies": {}, "variables": {}}

# Relay requests
relay_requests_block = {"policies": {}, "variables": {}}

# Block for jailing or slashing behaviors
jailing_slashing_block = {"policies": {}, "variables": {}}

# Reward disbursement
block_and_fee_rewards_block = {"policies": {}, "variables": {}}

# Undelegation and service unlinking block
undelegation_unservice_block = {"policies": {}, "variables": {}}

# Any entities leaving the system
leave_block = {"policies": {}, "variables": {}}

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
