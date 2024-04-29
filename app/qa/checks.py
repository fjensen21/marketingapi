from dataclasses import dataclass
from typing import Any, Dict, List, NoReturn, Tuple, Union

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


@dataclass
class PartialQAAd:
    id: int
    name: str
    ad_set_id: int
    campaign_id: int
    website_url: str
    cta: str
    extra_fields: Union[Dict[str, Any], None] = None


class QACheckCallback:
    def execute(self, ad: PartialQAAd) -> Union[CheckResponse, NoReturn]:
        raise NotImplementedError("Subclasses must implement execute function")


class CheckAdName(QACheckCallback):
    def __init__(self, expected_ad_name: str):
        self.expected_ad_name = expected_ad_name

    def execute(self, ad: PartialQAAd):
        if ad.name == self.expected_ad_name:
            return True, None

        return False, "Ad name does not match expected ad name."
