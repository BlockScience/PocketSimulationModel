event_map = {
    "servicer_shutdown_by_geozone_random": {
        "time": 182,
        "type": "servicer_shutdown",
        "attribute": "geozone",
        "attribute_value": "random",
    },
    "service_shutdown_random": {
        "time": 182,
        "type": "service_shutdown",
        "service": "random",
        "shutdown_time": 10,
    },
    "service_shutdown_random_t1": {
        "time": 182,
        "type": "service_shutdown",
        "service": "random",
        "shutdown_time": 1,
    },
    "service_shutdown_random_t7": {
        "time": 182,
        "type": "service_shutdown",
        "service": "random",
        "shutdown_time": 7,
    },
    "service_shutdown_random_t500": {
        "time": 182,
        "type": "service_shutdown",
        "service": "random",
        "shutdown_time": 500,
    },
    "service_join": {
        "time": 182,
        "type": "service_join",
    },
    "double_relays_1_service": {
        "time": 182,
        "type": "service_relay_multiply",
        "num_services": 1,
        "multiple": 2,
    },
    "double_relays_3_services": {
        "time": 182,
        "type": "service_relay_multiply",
        "num_services": 3,
        "multiple": 2,
    },
    "double_relays_5_services": {
        "time": 182,
        "type": "service_relay_multiply",
        "num_services": 5,
        "multiple": 2,
    },
    "oracle_shutdown": {
        "time": 182,
        "type": "oracle_shutdown",
    },
    "oracle_delay_constant_10": {
        "time": 182,
        "type": "oracle_delay_constant",
        "delay_time": 10,
    },
    "oracle_distortion_A_constant_30": {
        "time": 182,
        "type": "oracle_distortion_constant",
        "delay_time": 30,
        "mu": -3.1885519850880812,
        "sigma": 0.3638713191401966,
    },
}
