from app.qa.ad_qa_system import AdQASystem, Failure
from app.qa.checks import CheckAdName, ExpectedValues, PartialQAAd


def test_run_checks_with_single_check_and_failures():
    qa_system = AdQASystem()
    check = CheckAdName("ad1")
    qa_system.register_check(check)
    ads = [
        PartialQAAd(
            id=1,
            name="ad1",
            ad_set_id=1,
            campaign_id=1,
            platform="Meta",
            website_url="example.com",
            cta="cta1",
        ),
        PartialQAAd(
            id=3,
            name="ad2",
            ad_set_id=1,
            campaign_id=1,
            platform="Meta",
            website_url="example.com",
            cta="cta1",
        ),
    ]

    result = qa_system.run_checks(ads)

    expected_failure = Failure(ads[1])
    expected_failure.reasons.append("Ad name does not match expected ad name.")
    assert result == (False, [expected_failure])


def test_run_checks_with_single_check_success():
    qa_system = AdQASystem()
    check = CheckAdName("ad1")
    qa_system.register_check(check)
    ads = [
        PartialQAAd(
            id=1,
            name="ad1",
            ad_set_id=1,
            campaign_id=1,
            platform="Meta",
            website_url="example.com",
            cta="cta1",
        ),
        PartialQAAd(
            id=2,
            name="ad1",
            ad_set_id=1,
            campaign_id=1,
            platform="Meta",
            website_url="example.com",
            cta="cta1",
        ),
    ]

    result = qa_system.run_checks(ads)
    assert result == (True, None)


def test_run_default_checks_with_all_failures():
    ad = PartialQAAd(
        id=1,
        name="ad1",
        ad_set_id=1,
        campaign_id=1,
        platform="Meta",
        website_url="example.com",
        cta="cta1",
    )
    qa_system = AdQASystem()
    expected_values: ExpectedValues = ExpectedValues(
        ad_name="ad2", cta="cta2", website_url="example2.com", campaigns={2: [1]}
    )
    qa_system.register_default_checks(expected_values)
    result = qa_system.run_checks([ad])
    expected_failure = Failure(ad)
    expected_failure.reasons = [
        "Ad name does not match expected ad name.",
        "CTA does not match expected CTA.",
        "Website URL does not match expected Website URL.",
        "Ad not expected in campaign and ad set."
    ]
    expected = (False, [expected_failure])
    assert expected == result


def test_run_default_checks_with_success():
    ad = PartialQAAd(
        id=1,
        name="ad1",
        ad_set_id=1,
        campaign_id=1,
        platform="Meta",
        website_url="example.com",
        cta="cta1",
    )
    qa_system = AdQASystem()
    expected_values: ExpectedValues = ExpectedValues(
        ad_name="ad1", cta="cta1", website_url="example.com", campaigns={1: [1]}
    )
    qa_system.register_default_checks(expected_values)
    result = qa_system.run_checks([ad])
    expected = (True, None)
    assert expected == result
