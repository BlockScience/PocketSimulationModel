from typing import TypedDict, Dict
from ..types import ServiceEntityType

service_leave_space = TypedDict(
    "Service Leave Space",
    {
        "services": Dict[ServiceEntityType, bool],
    },
)

service_join_space = TypedDict(
    "Service Join Space", {"name": str, "portal_api_prefix": str, "service_id": str}
)


service_entity_space = TypedDict(
    "Service Entity Space",
    {
        "application": ServiceEntityType,
    },
)
