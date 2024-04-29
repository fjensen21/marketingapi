from typing import Any, Dict, List, Tuple, Union
from dataclasses import dataclass

from app.qa.checks import QACheckCallback, PartialQAAd


class Failure:
    def __init__(self, ad: PartialQAAd, reasons: List[str] = []):
        self.ad = ad
        self.reasons = reasons


Pass = Tuple[bool, None]
Fail = Tuple[bool, List[Failure]]


class AdQASystem:
    def __init__(self, run_default_checks=True):
        self.checks: List[QACheckCallback] = []
        if run_default_checks:
            self.checks.append

    def run_checks(self, ads: List[PartialQAAd]) -> Union[Pass, Fail]:
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
