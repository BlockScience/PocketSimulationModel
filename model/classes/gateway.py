from ..types import StakeStatusType, ApplicationEntityType, uPOKTType
from typing import List


class Gateway:
    id_number = 0

    def __init__(
        self,
        name: str,
        stake_status: StakeStatusType,
        delegators: List[ApplicationEntityType],
        pokt_holdings: uPOKTType,
        staked_pokt: uPOKTType,
    ):
        self.id_number = Gateway.id_number
        Gateway.id_number += 1
        self.name = name
        self.stake_status = stake_status
        self.delegators = delegators
        self.pokt_holdings = pokt_holdings
        self.staked_pokt = staked_pokt
