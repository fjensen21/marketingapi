import pytest
from app.qa.checks import CheckAdName, PartialQAAd


@pytest.fixture
def default_ad_instance():
    ad = PartialQAAd(
        id=1,
        name="ad1",
        ad_set_id=1,
        campaign_id=1,
        website_url="example.com",
        cta="cta1",
    )
    return ad


def test_check_ad_name_with_correct_expected(default_ad_instance):
    check = CheckAdName("ad1")
    result = check.execute(default_ad_instance)
    assert result == (True, None)


def test_check_ad_name_with_incorrect_expected(default_ad_instance):
    check = CheckAdName("ad2")
    result = check.execute(default_ad_instance)
    assert result == (False, "Ad name does not match expected ad name.")
