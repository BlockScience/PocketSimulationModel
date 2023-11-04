from typing import TypedDict, List, Dict
from ..types import (
    PublicKeyType,
    uPOKTType,
    ServiceURLType,
    StakeStatusType,
    BlockHeightType,
    GatewayEntityType,
)

gateway_leave_space = TypedDict(
    "Gateway Leave Space",
    {
        "gateways": Dict[GatewayEntityType, bool],
    },
)


gateway_join_space = TypedDict(
    "Gateway Stake Space",
    {
        "name": str,
        "stake_amount": uPOKTType,  # The amount of uPOKT in escrow (i.e. a security deposit)
        "personal_holdings": uPOKTType,  # Unstaked POKT the application personally holds
    },
)

gateway_entity_space = TypedDict(
    "Gateway Entity Space",
    {
        "gateway": GatewayEntityType,
    },
)

gateway_registration_space = TypedDict(
    "Gateway Registration Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the Gateway account
        "stake_amount": uPOKTType,  # The amount of uPOKT in escrow (i.e. a security deposit)
        "service_url": ServiceURLType,  # The API endpoint where the Gateway service is provided
    },
)

gateway_unregistration_space = TypedDict(
    "Gateway Unregistration Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the Gateway account
    },
)

gateway_relay_request_space = TypedDict(
    "Gateway Relay Request Space",
    {
        "payload": dict,  # the data payload of the request
        "meta": dict,  # metadata for the relay request
        "proof": dict,  # the authentication scheme needed for work
        "application_address": PublicKeyType,
        "gateway_address": PublicKeyType,
    },
)
modify_gateway_pokt_space = TypedDict(
    "Modify Gateway POKT Space",
    {
        "public_key": PublicKeyType,
        "amount": uPOKTType,
    },
)

gateway_stake_status_space = TypedDict(
    "Servicer Stake Status Space",
    {
        "address": PublicKeyType,  # address of the unstaking servicer
        "height": BlockHeightType,
        "status": StakeStatusType,
    },
)

return_gateway_stake_space = TypedDict(
    "Return Gateway Stake Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the custodial account
        "amount": uPOKTType,
    },
)
