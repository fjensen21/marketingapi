from dataclasses import dataclass
from typing import Any, Dict, List, NoReturn, Optional, Tuple, TypedDict, Union

from app.models import Ad

CheckResponse = Tuple[bool, Union[None, str]]

DEFAULT_CHECKS = []


@dataclass
class ExpectedValues:
    ad_name: str
    website_url: str
    cta: str
    campaigns: Dict[
        int, List[int]
    ]  # dictionary of campaign ids and corresponding adset ids


class DefaultChecks(TypedDict):
    ad_name: bool
    cta: bool
    website_url: bool


# @dataclass
# class PartialQAAd:
#     id: int
#     name: str
#     ad_set_id: int
#     campaign_id: int
#     platform: str
#     website_url: str
#     cta: str
#     ad_set_name: Optional[str] = None
#     campaign_name: Optional[str] = None
#     extra_fields: Union[Dict[str, Any], None] = None


class QACheckCallback:
    def execute(self, ad: Ad) -> Union[CheckResponse, NoReturn]:
        raise NotImplementedError("Subclasses must implement execute function")


class CheckAdName(QACheckCallback):
    def __init__(self, expected_ad_name: str):
        self.expected_ad_name = expected_ad_name

    def execute(self, ad: Ad):
        if ad.name == self.expected_ad_name:
            return True, None

        return False, "Ad name does not match expected ad name."


class CheckCTA(QACheckCallback):
    def __init__(self, expected_cta: str):
        self.expected_cta = expected_cta

    def execute(self, ad: Ad):
        if ad.cta == self.expected_cta:
            return True, None

        return False, "CTA does not match expected CTA."


class CheckWebsiteURL(QACheckCallback):
    def __init__(self, expected_website_url: str):
        self.expected_website_url = expected_website_url

    def execute(self, ad: Ad):
        if ad.website_url == self.expected_website_url:
            return True, None

        return False, "Website URL does not match expected Website URL."


class CheckCorrectCampaignAndAdSet(QACheckCallback):
    def __init__(self, expected_campaign_structure: Dict[int, List[int]]):
        self.expected_campaign_structure = expected_campaign_structure

    def execute(self, ad: Ad):
        if (
            ad.campaign_id in self.expected_campaign_structure
            and ad.ad_set_id in self.expected_campaign_structure[ad.campaign_id]
        ):
            return True, None
        return False, "Ad not expected in campaign and ad set."
