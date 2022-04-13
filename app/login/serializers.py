# library imports
from flask_restplus import Resource, fields

# module imports
from app import api


login = api.model("login", {
    "email": fields.String(required=True, description="Enter email"),
    "role": fields.String(required=True, description="Enter user role"),
    "password": fields.String(required=True, description="Enter password"),
})

