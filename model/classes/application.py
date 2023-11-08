from ..types import (
    PublicKeyType,
    uPOKTType,
    ServiceType,
    GeoZoneType,
    StakeStatusType,
    BlockHeightType,
    GatewayEntityType,
)
from typing import List


class Application:
    id_number = 0

    def __init__(
        self,
        name: str,
        pokt_holdings: uPOKTType,
        staked_pokt: uPOKTType,
        services: List[ServiceType],
        geo_zone: GeoZoneType,
        number_of_services: int,
        stake_status: StakeStatusType,
        unstaking_height: BlockHeightType,
        delegate: GatewayEntityType,
        uses_gateway: bool,
    ):
        self.id_number = Application.id_number
        Application.id_number += 1
        self.name = name
        self.public_key = self
        self.pokt_holdings = pokt_holdings
        self.staked_pokt = staked_pokt
        self.services = services
        self.geo_zone = geo_zone
        self.number_of_services = number_of_services
        self.stake_status = stake_status
        self.unstaking_height = unstaking_height
        self.delegate = delegate

        # Behavioral assumption of whether an application uses gateways or not
        self.uses_gateway = uses_gateway
