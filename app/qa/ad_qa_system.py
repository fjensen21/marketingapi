from typing import List, Tuple, Union

from pydantic import BaseModel

from app.models import Ad
from app.qa.checks import (
    CheckAdName,
    CheckCTA,
    CheckCorrectCampaignAndAdSet,
    CheckWebsiteURL,
    ExpectedValues,
    QACheckCallback,
)


class Failure(BaseModel):
    def __init__(self, ad: Ad):
        self.ad = ad
        self.reasons = []

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.ad == value.ad and sorted(self.reasons) == sorted(value.reasons)
        return False


Pass = Tuple[bool, None]
Fail = Tuple[bool, List[Failure]]


class AdQASystem:
    def __init__(self):
        self.checks: List[QACheckCallback] = []

    def run_checks(self, ads: List[Ad]) -> Union[Pass, Fail]:
        failures: List[Failure] = []
        for ad in ads:
            failure = Failure(ad)
            for check in self.checks:
                success, message = check.execute(ad)
                if not success:
                    assert isinstance(message, str)
                    failure.reasons.append(message)
            if failure.reasons:
                failures.append(failure)

        if failures:
            return False, failures
        return True, None

    def register_check(self, check: QACheckCallback):
        self.checks.append(check)

    def register_default_checks(
        self,
        expected_values: ExpectedValues,
        check_cta=True,
        check_ad_name=True,
        check_website_url=True,
        check_correct_campaign_and_ad_set=True,
    ):
        if check_ad_name:
            self.register_check(CheckAdName(expected_values.ad_name))

        if check_cta:
            self.register_check(CheckCTA(expected_values.cta))

        if check_website_url:
            self.register_check(CheckWebsiteURL(expected_values.website_url))

        if check_correct_campaign_and_ad_set:
            self.register_check(CheckCorrectCampaignAndAdSet(expected_values.campaigns))
