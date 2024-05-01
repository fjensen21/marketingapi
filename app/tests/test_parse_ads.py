import io
import codecs

from app.fileparse.parse_ads import AdParser
from app.models import Ad

HEADERS = [
    "id",
    "name",
    "platform",
    "ad_set_id",
    "campaign_id",
    "website_url",
    "campaign_name",
    "ad_set_name",
    "cta",
]


def generate_csv_from_rows(rows, headers) -> io.BytesIO:
    csv_string = f"{','.join(headers)}\n"
    for row in rows:
        csv_string += ",".join(row)
        csv_string += "\n"

    return io.BytesIO(codecs.encode(csv_string, "utf-8"))


def test_parse_two_ads_no_errors():
    rows = [
        ["1", "ad1", "Meta", "1", "1", "example1.com", "campaign1", "adset1", "cta1"],
        ["2", "ad2", "Meta", "2", "2", "example2.com", "campaign2", "adset2", "cta2"],
    ]
    csv = generate_csv_from_rows(rows, HEADERS)
    ads = AdParser.parse(csv, retain_extra_fields=False)
    expected_ads = [
        Ad(
            id=1,
            name="ad1",
            platform="Meta",
            ad_set_id=1,
            campaign_id=1,
            website_url="example1.com",
            cta="cta1",
            campaign_name="campaign1",
            ad_set_name="adset1",
        ),
        Ad(
            id=2,
            name="ad2",
            platform="Meta",
            ad_set_id=2,
            campaign_id=2,
            website_url="example2.com",
            cta="cta2",
            campaign_name="campaign2",
            ad_set_name="adset2",
        ),
    ]

    assert ads == expected_ads


def test_parse_two_ads_no_errors_extra_field():
    rows = [
        [
            "1",
            "ad1",
            "Meta",
            "1",
            "1",
            "example1.com",
            "campaign1",
            "adset1",
            "cta1",
            "1",
        ],
        [
            "2",
            "ad2",
            "Meta",
            "2",
            "2",
            "example2.com",
            "campaign2",
            "adset2",
            "cta2",
            "2",
        ],
    ]
    headers_with_extra = [header for header in HEADERS]
    headers_with_extra.append("extra")
    csv = generate_csv_from_rows(rows, headers_with_extra)
    ads = AdParser.parse(csv, retain_extra_fields=True)
    expected_ads = [
        Ad(
            id=1,
            name="ad1",
            platform="Meta",
            ad_set_id=1,
            campaign_id=1,
            website_url="example1.com",
            cta="cta1",
            campaign_name="campaign1",
            ad_set_name="adset1",
            extra_fields={"extra": "1"},
        ),
        Ad(
            id=2,
            name="ad2",
            platform="Meta",
            ad_set_id=2,
            campaign_id=2,
            website_url="example2.com",
            cta="cta2",
            campaign_name="campaign2",
            ad_set_name="adset2",
            extra_fields={"extra": "2"},
        ),
    ]

    assert ads == expected_ads
