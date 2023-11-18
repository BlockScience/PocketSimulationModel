from copy import deepcopy
from model.classes import Application, DAO, Gateway, Service, Servicer, Validator

config_option_map = {
    "Test": {
        "Geozones": "Test",
        "Applications": "Test",
        "DAO": "Test",
        "Gateways": "Test",
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
    state["Gateways"] = gateways_config[config_option["Gateways"]]
    state["Services"] = service_config[config_option["Services"]]
    state["Servicers"] = servicers_config[config_option["Servicers"]]
    state["Validators"] = validators_config[config_option["Validators"]]
    state["height"] = 0
    state["day"] = 0
    state["Treasury"] = None
    state["Sessions"] = []
    state["relay_fees"] = 0
    state["total_relays"] = None
    state["processed_relays"] = None
    state["pokt_price_true"] = 0.06
    state["pokt_price_oracle"] = 0.06
    state["n_transactions"] = None
    state["relay_log"] = None

    state = deepcopy(state)
    return state


geo_zones_config = {"Test": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]}

application_config = {
    "Test": [
        Application(
            name="A1",
            pokt_holdings=1000,
            staked_pokt=1000,
            services=[],
            geo_zone="Zone 1",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),
        Application(
            name="A2",
            pokt_holdings=5000,
            staked_pokt=1000,
            services=[],
            geo_zone="Zone 2",
            number_of_services=2,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=False,
        ),
        Application(
            name="A3",
            pokt_holdings=3000,
            staked_pokt=1000,
            services=[],
            geo_zone="Zone 3",
            number_of_services=1,
            stake_status="Staked",
            unstaking_height=None,
            delegate=None,
            uses_gateway=True,
        ),
    ]
}

dao_config = {"Test": DAO(pokt_holdings=100000)}

gateways_config = {
    "Test": [
        Gateway(
            name="P1",
            stake_status="Staked",
            delegators=[],
            pokt_holdings=100,
            staked_pokt=100,
        )
    ]
}

service_config = {
    "Test": [
        Service(
            name="S{}".format(x),
            gateway_api_prefix="S{}".format(x),
            service_id="S{}".format(x),
            servicers=[],
        )
        for x in range(1, 9)
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
            pokt_holdings=6000,
            staked_pokt=14000,
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
