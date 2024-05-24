from typing import List, Optional
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
import uvicorn

from app.fileparse.parse_ads import AdParser
from app.models import Ad
from app.qa.ad_qa_system import AdQASystem
from app.qa.checks import ExpectedValues

app = FastAPI()


origins = [
    "http://localhost:3000",
    "https://marketingtools.finnjensen.io",
    "https://www.marketingtools.finnjensen.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParseAdsConfig(BaseModel):
    retain_extra_fields: bool


def checker(config: str = Form(...)):
    try:
        return ParseAdsConfig.model_validate_json(config)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@app.get("/")
def hello_world():
    return "Hello to the world, deployed with action"


@app.post("/v1/upload/parseads")
def parse_ads_from_file(
    file: UploadFile = File(...), config: ParseAdsConfig = Depends(checker)
):
    retain_extra_fields = config.retain_extra_fields

    try:
        ads = AdParser.parse(file.file, retain_extra_fields)
        return {"succcess": True, "message": "Ads successfully parsed.", "ads": ads}
    except KeyError:
        return {
            "success": False,
            "message": "There was an error parsing due to incorrect field names or not including all required fields.",
        }


# class FailureResponse(BaseModel):
#     ad: Ad
#     reasons: List[str]


@app.post("/v1/qa/ads")
def qa_ads(ads: List[Ad], expected_values: ExpectedValues):
    qa_system = AdQASystem()
    qa_system.register_default_checks(expected_values=expected_values)
    passed, failures = qa_system.run_checks(ads)

    if not failures:
        return {"passed": passed, "failures": failures}

    return {
        "passed": passed,
        "failures": failures,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
