from typing import Any, Dict, Optional, Union

from pydantic import BaseModel


class Ad(BaseModel):
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

    def __hash__(self):
        # Create a hash based on the id attribute
        return hash(self.id)

    def __eq__(self, other):
        # Check equality based on the id attribute
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False
