# marketingapi

Open source api for common marketing tasks like ad builds and QAs

# API

## File Parse API

Currently the File Parse API is used to get Ads from a file upload. This method can be used if you don't have API access to the platform you wish to upload ads from. You can also upload ads from a platform not supported by the PlatformAPI as long as you can adapt them to fit the required format for uploaded files.

Currently this API only supports CSV uploads.

### Endpoints

#### POST /upload/parseads

Used to parse out ads from a file. When a file is uploaded the file is turned into ad objects which are passed back as JSON. Currently this endpoint only supports CSV uploads.

Both file and platform should be passed as FormData as part of a multipart Form.

**Parameters**
file: The CSV file to be uploaded
config: Config object including whether or not you want to retain extra fields

Sample Config

```bash
{
    "retain_extra_fields": true
}
```

**Responses**

**Sample Success Response**

All fields will be parsed and any extra columns in the csv will be parsed into the extra fields dictionary.

```bash
{
    "success": true,
    "message": "Ads successfully parsed",
    "ads": [
    {
        "id": 1,
        "name": "ad1",
        "ad_set_id": 1,
        "campaign_id": 1,
        "platform": "Meta",
        "website_url": "example.com",
        "cta": "cta1",
        "campaign_name": "Campaign1",
        "ad_set_name": "AdSet1"
        "extra_fields": {"otherfield": "value"}
    }
    ]
}
```
