import pytest
from app.qa.checks import (
    CheckAdName,
    CheckCTA,
    CheckCorrectCampaignAndAdSet,
    CheckWebsiteURL,
    PartialQAAd,
)


@pytest.fixture
def default_ad_instance():
    ad = PartialQAAd(
        id=1,
        name="ad1",
        ad_set_id=1,
        campaign_id=1,
        platform="Meta",
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


def test_check_cta_with_correct_expected(default_ad_instance):
    check = CheckCTA("cta1")
    result = check.execute(default_ad_instance)
    assert result == (True, None)


def test_check_cta_with_incorrect_expected(default_ad_instance):
    check = CheckCTA("cta2")
    result = check.execute(default_ad_instance)
    assert result == (False, "CTA does not match expected CTA.")


def test_check_landing_page_with_correct_expected(default_ad_instance):
    check = CheckWebsiteURL("example.com")
    result = check.execute(default_ad_instance)
    assert result == (True, None)


def test_check_landing_page_with_incorrect_expected(default_ad_instance):
    check = CheckWebsiteURL("example1.com")
    result = check.execute(default_ad_instance)
    assert result == (False, "Website URL does not match expected Website URL.")


def test_check_correct_campaign_and_ad_set_with_incorrect_ad_set(default_ad_instance):
    check = CheckCorrectCampaignAndAdSet({1: [2]})
    result = check.execute(default_ad_instance)
    assert result == (False, "Ad not expected in campaign and ad set.")


def test_check_correct_campaign_and_ad_set_with_incorrect_campaign(
    default_ad_instance,
):
    check = CheckCorrectCampaignAndAdSet({2: [1]})
    result = check.execute(default_ad_instance)
    assert result == (False, "Ad not expected in campaign and ad set.")


def test_check_correct_campaign_and_ad_set_with_correct_campaign_ad_set(
    default_ad_instance,
):
    check = CheckCorrectCampaignAndAdSet({1: [1]})
    result = check.execute(default_ad_instance)
    assert result == (True, None) 
