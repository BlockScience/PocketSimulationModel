from .meta import p_update_time, s_update_height, s_update_day


meta_update_block = {
    "policies": {
        "t": p_update_time,
    },
    "variables": {"day": s_update_day, "height": s_update_height},
}


psub_blocks = [meta_update_block]
