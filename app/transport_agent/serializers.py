# library imports
from flask_restplus import Resource, fields

# module imports
from app import api, transport_agent


transport_agent = api.model("transport_agent", {
    "first_name" : fields.String(required=True, description="first_name"),
    "last_name" : fields.String(required=True, description="last_name"),
    "email" : fields.String(required=False, description="email"),
    "role" : fields.String(required=False, description="role"),
    "license_no" : fields.String(required=True, description="license_no"),
    "about" : fields.String(required=False, description="about"),
    'agent_details': fields.List(fields.Raw(), description="agent_details"),
    'vehicle_details': fields.List(fields.Raw(), description="vehicle_details")
    })


profile = api.model("profile", {
    "email" : fields.String(required=True, description="email")
    })

