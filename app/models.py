from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


@dataclass
class Ad:
    id: int
    name: str
    ad_set_id: int
    campaign_id: int
    platform: str
    website_url: str
    cta: str
    ad_set_name: Optional[str] = None
    campaign_name: Optional[str] = None
    extra_fields: Union[Dict[str, Any], None] = None
