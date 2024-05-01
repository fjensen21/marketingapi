import codecs
import csv
from typing import BinaryIO, List

from app.models import Ad


class AdParser:
    """
    Parse ads from a CSV files into ad objects
    """

    @classmethod
    def parse(cls, file: BinaryIO, retain_extra_fields=True) -> List[Ad]:
        reader = AdReader(file)
        ads = []
        for ad in reader:
            if not retain_extra_fields:
                ad.extra_fields = None
            ads.append(ad)
        return ads


class AdReader(object):
    """
    Handle the conversion from csv rows to Ad objects.
    """

    def __init__(self, file: BinaryIO):
        self.file = file

    def __iter__(self):
        encoding = "utf-8-sig"
        reader = csv.DictReader(codecs.iterdecode(self.file, encoding))

        for row in reader:
            ad = AdReader.parse_ad_from_row(row)
            yield ad

        self.file.close()

    @classmethod
    def parse_ad_from_row(cls, row):
        required_fields = {
            "id",
            "name",
            "platform",
            "ad_set_id",
            "campaign_id",
            "website_url",
            "campaign_name",
            "ad_set_name",
            "cta",
        }

        for field in required_fields:
            if field not in row:
                raise KeyError

        extra_fields = {}
        for field in row:
            if field not in required_fields:
                extra_fields[field] = str(row[field])

        ad = Ad(
            id=int(row["id"]),
            name=row["name"],
            ad_set_id=int(row["ad_set_id"]),
            campaign_id=int(row["campaign_id"]),
            website_url=row["website_url"],
            campaign_name=row["campaign_name"],
            ad_set_name=row["ad_set_name"],
            platform=row["platform"],
            cta=row["cta"],
            extra_fields=extra_fields,
        )
        return ad
