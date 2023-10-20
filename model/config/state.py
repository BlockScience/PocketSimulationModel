from copy import deepcopy
from model.classes import Application, DAO, Portal, Service, Servicer, Validator

config_option_map = {
    "Test": {
        "Geozones": "Test",
        "Applications": "Test",
        "DAO": "Test",
        "Portals": "Test",
        "Services": "Test",
        "Servicers": "Test",
        "Validators": "Test",
    }
}


def build_state(config_option):
    config_option = config_option_map[config_option]
    state = {}

    state["Geozones"] = geo_zones_config[config_option["Geozones"]]
    state["Applications"] = application_config[config_option["Applications"]]
    state["DAO"] = dao_config[config_option["DAO"]]
    state["Portals"] = portals_config[config_option["Portals"]]
    state["Services"] = service_config[config_option["Services"]]
    state["Servicers"] = servicers_config[config_option["Servicers"]]
    state["Validators"] = validators_config[config_option["Validators"]]
    state["height"] = 0
    state["day"] = 0
    state["Treasury"] = None
    state["Sessions"] = []

    state = deepcopy(state)
    return state


geo_zones_config = {"Test": ["G1", "G2", "G3"]}

application_config = {
    "Test": [
        Application(
            name="A1",
            pokt_holdings=1000,
            staked_pokt=1000,
            services=["S1", "S2"],
            geo_zone="G1",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
        ),
        Application(
            name="A2",
            pokt_holdings=5000,
            staked_pokt=1000,
            services=["S2", "S3"],
            geo_zone="G2",
            number_of_services=2,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
        ),
        Application(
            name="A3",
            pokt_holdings=3000,
            staked_pokt=1000,
            services=["S1", "S3"],
            geo_zone="G3",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate="P1",
        ),
    ]
}

dao_config = {"Test": DAO(pokt_holdings=100000)}

portals_config = {
    "Test": [
        Portal(
            name="P1",
            stake_status="Staked",
            delegators=["A3"],
            pokt_holdings=100,
            staked_pokt=100,
        )
    ]
}

service_config = {
    "Test": [
        Service(name="S1", portal_api_prefix="S1", service_id="S1", servicers=[]),
        Service(name="S2", portal_api_prefix="S2", service_id="S2", servicers=[]),
        Service(name="S3", portal_api_prefix="S3", service_id="S3", servicers=[]),
    ]
}

servicers_config = {"Test": []}

for i in range(1, 6):
    servicers_config["Test"].append(
        Servicer(
            name="X{}".format(i),
            servicer_salary=0,
            report_card=None,
            test_scores=None,
            pokt_holdings=1000,
            staked_pokt=1000,
            service_url=None,
            services=[],
            geo_zone="G{}".format(i % 3 + 1),
            operator_public_key=None,
            pause_height=None,
            stake_status="Staked",
            unstaking_height=None,
        )
    )

validators_config = {
    "Test": [
        Validator(
            name="Mega Validator",
            pokt_holdings=1000,
            staked_pokt=1000,
            service_url=None,
            operator_public_key=None,
            stake_status="Staked",
        )
    ]
}
