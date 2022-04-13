# library imports
from flask_restplus import Resource, fields

# module imports
from app import api, event_module


event_module = api.model("event_module", {
    "event_name" : fields.String(required=True, description="event_name"),
    "event_location" : fields.String(required=True, description="event_location"),
    "organizer_name" : fields.String(required=True, description="organizer_name"),
    "mobile" : fields.String(required=False, description="mobile"),
    "whatsapp" : fields.String(required=True, description="whatsapp"),
    "alternate_contact_person" : fields.String(required=False, description="alternate_contact_person"),
    "alternate_contact_number" : fields.String(required=False, description="alternate_contact_number"),
    "alternate_whatsapp" : fields.String(required=True, description="alternate_whatsapp"),
    "email" : fields.String(required=False, description="email"),
    "about" : fields.String(required=False, description="about")
    # 'organizer_details': fields.List(fields.Raw(), description="organizer_details"),
    # 'vehicle_details': fields.List(fields.Raw(), description="vehicle_details")
    })


profile = api.model("profile", {
    "email" : fields.String(required=True, description="email")
    })
