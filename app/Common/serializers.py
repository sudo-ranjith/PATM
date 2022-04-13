from flask_restplus import Resource, fields

# module imports
from app import api

# response model
response_api_model = api.model("response", {
    "status": fields.String(description="Status of the response - success or failure"),
    "message": fields.String(description="Message for the response"),
    "more_info": fields.String(description="More information about the response - mainly useful for error info"),
    "data": fields.List(fields.Raw, description="Retrieved data - if no data [] is returned")
})

# upload model
# upload_model = api.model("upload", {
#     # upload image file
#     "image": fields.File(description="Image file to be uploaded")
#     # "file": fields.String(description="File to be uploaded")
# })
