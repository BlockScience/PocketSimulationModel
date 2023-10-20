from ..types import (
    uPOKTType,
    ServicerReportCardType,
    ServicerTestScoresType,
    PublicKeyType,
    GeoZoneType,
    ServiceType,
    ServiceURLType,
    BlockHeightType,
    StakeStatusType,
)
from typing import List


class Servicer:
    id_number = 0
    def __init__(
        self,
        name: str,
        servicer_salary: uPOKTType,
        report_card: ServicerReportCardType,
        test_scores: ServicerTestScoresType,
        pokt_holdings: uPOKTType,
        staked_pokt: uPOKTType,
        service_url: ServiceURLType,
        services: List[ServiceType],
        geo_zone: GeoZoneType,
        operator_public_key: PublicKeyType,
        pause_height: BlockHeightType,
        stake_status: StakeStatusType,
        unstaking_height: BlockHeightType,
    ):
        self.id_number = Servicer.id_number
        Servicer.id_number += 1
        self.name = name
        self.public_key = self
        self.servicer_salary = servicer_salary
        self.report_card = report_card
        self.test_scores = test_scores
        self.pokt_holdings = pokt_holdings
        self.staked_pokt = staked_pokt
        self.service_url = service_url
        self.services = services
        self.geo_zone = geo_zone
        self.operator_public_key = operator_public_key
        self.pause_height = pause_height
        self.stake_status = stake_status
        self.unkstaking_height = unstaking_height
