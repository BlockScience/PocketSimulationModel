from ..types import PublicKeyType, uPOKTType, ServiceURLType, StakeStatusType


class Validator:
    def __init__(
        self,
        name: str,
        pokt_holdings: uPOKTType,
        staked_pokt: uPOKTType,
        service_url: ServiceURLType,
        operator_public_key: PublicKeyType,
        stake_status: StakeStatusType,
    ):
        self.name = name
        self.public_key = self
        self.pokt_holdings = pokt_holdings
        self.staked_pokt = staked_pokt
        self.service_url = service_url
        self.operator_public_key = operator_public_key
        self.stake_status = stake_status
