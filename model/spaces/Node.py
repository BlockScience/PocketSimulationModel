from typing import TypedDict
from ..types import PublicKeyType, BlockHeightType

unjail_node_space = TypedDict(
    "Unjail Node Space",
    {
        "node_address": PublicKeyType,
        "block_height": BlockHeightType,
    },
)
