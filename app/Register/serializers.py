# library imports
from flask_restplus import Resource, fields

# module imports
from app import api


register = api.model("register", {
    "first_name": fields.String(required=True, description="Enter first_name"),
    "last_name": fields.String(required=True, description="Enter last_name"),
    "email": fields.String(required=True, description="Enter email_address"),
    "mobile": fields.Integer(required=True, description="Enter phone_number"),
    "role": fields.String(required=True, description="Enter user role"),
    "password": fields.String(required=True, description="Enter password"),
})
