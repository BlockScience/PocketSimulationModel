from typing import TypedDict
from ..types import uPOKTType

dao_block_reward_space = TypedDict("DAO Block Reward Space", {"reward_amount": int})

modify_dao_pokt_space = TypedDict("Modify DAO POKT Space", {"amount": uPOKTType})
