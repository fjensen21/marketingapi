from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError

from app.fileparse.parse_ads import AdParser

app = FastAPI()


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


@app.get("v1/upload/parseads")
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
