from typing import TypedDict, List, Dict
from ..types import (
    PublicKeyType,
    uPOKTType,
    ServiceType,
    GeoZoneType,
    ActorType,
    AddressType,
    BlockHeightType,
    StakeStatusType,
    ApplicationEntityType,
    SessionType,
)

application_leave_space = TypedDict(
    "Application Leave Space",
    {
        "applications": Dict[ApplicationEntityType, bool],
    },
)

new_session_space = TypedDict(
    "New Session Space",
    {
        "session": SessionType,
    },
)

application_join_space = TypedDict(
    "Application Join Space",
    {
        "name": str,
        "stake_amount": uPOKTType,  # The amount of uPOKT in escrow (i.e. a security deposit)
        "geo_zone": GeoZoneType,  # The physical geo-location identifier this Servicer registered in
        "number_servicers": int,  # The number of Servicers requested per session
        "personal_holdings": uPOKTType,  # Unstaked POKT the application personally holds
    },
)

application_entity_space = TypedDict(
    "Application Entity Space",
    {
        "application": ApplicationEntityType,
    },
)

application_stake_space = TypedDict(
    "Application Stake Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the Application
        "stake_amount": uPOKTType,  # The amount of uPOKT in escrow (i.e. a security deposit)
        "services": List[ServiceType],  # The flavor(s) of Web3 hosted by this Servicer
        "geo_zone": GeoZoneType,  # The physical geo-location identifier this Servicer registered in
        "number_servicers": int,  # The number of Servicers requested per session
    },
)


modify_application_pokt_space = TypedDict(
    "Modify Application POKT Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the custodial account
        "amount": uPOKTType,  # The amount of uPOKT to modify by
    },
)


application_param_update_space = TypedDict(
    "Application Param Update Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the Application
        "services": List[ServiceType],  # The flavor(s) of Web3 hosted by this Servicer
        "geo_zone": GeoZoneType,  # The physical geo-location identifier this Servicer registered in
        "number_servicers": int,  # The number of Servicers requested per session
    },
)

application_unstake_space = TypedDict(
    "Application Unstake Space",
    {
        "actor_type": ActorType,
        "address": AddressType,
        "signer": AddressType,
    },
)

application_delegate_to_gateway_space = TypedDict(
    "Application Delegate to Gateway Space",
    {
        "application_public_key": PublicKeyType,  # The cryptographic ID of the Application
        "gateway_public_key": PublicKeyType,  # The cryptographic ID of the Gateway
    },
)

application_undelegation_space = TypedDict(
    "Application Undelegation Space",
    {
        "application_public_key": PublicKeyType,  # The cryptographic ID of the Application
        "gateway_public_key": PublicKeyType,  # The cryptographic ID of the Gateway
    },
)
return_application_stake_space = TypedDict(
    "Return Application Stake Space",
    {
        "public_key": PublicKeyType,  # The public cryptographic id of the custodial account
        "amount": uPOKTType,
    },
)

submit_relay_request_space = TypedDict(
    "Submit Relay Request Space",
    {
        "payload": dict,  # the data payload of the request
        "meta": dict,  # metadata for the relay request
        "proof": dict,  # the authentication scheme needed for work
        "application_address": PublicKeyType,
    },
)

application_stake_status_space = TypedDict(
    "Application Stake Status Space",
    {
        "address": PublicKeyType,  # address of the unstaking application
        "height": BlockHeightType,
        "status": StakeStatusType,
    },
)
