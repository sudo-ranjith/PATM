# library imports
from flask_restplus import Resource, fields

# module imports
from app import api


purchase_module = api.model("purchase_module", {
    "vendor_name" : fields.String(required=True, description="vendor_name"),
    "vendor_location" : fields.String(required=True, description="vendor_location"),
    "vendor_phone" : fields.String(required=True, description="vendor_phone"),
    "vendor_mail" : fields.String(required=True, description="vendor_mail"),
    "order_date" : fields.String(required=True, description="order_date"),
    "contact_person" : fields.String(required=True, description="contact_person"),
    "telephone_number" : fields.String(required=True, description="telephone_number"),
    
    "product_name" : fields.String(required=True, description="product_name"),
    "price" : fields.String(required=True, description="price"),
    "quantity" : fields.String(required=True, description="quantity"),
    "total_amount" : fields.String(required=True, description="total_amount"),
    "payment_status" : fields.String(required=True, description="payment_status"),
    "order_status" : fields.String(required=True, description="order_status"),
    "expected_delivery_date" : fields.String(required=True, description="expected_delivery_date"),
    "shipping_address" : fields.String(required=True, description="shipping_address"),
    "for_event" : fields.String(required=False, description="for_event"),
    "ordered_by" : fields.String(required=True, description="ordered_by"),
    "approved_by" : fields.String(required=True, description="approved_by"),
    "approve_status" : fields.Integer(required=True, description="approve_status"),

    'others': fields.String(required=False, description="others")
    })

approval = api.model("approval", {
    "approve_status" : fields.Integer(required=True, description="approval"),
    '_id': fields.String(required=True, description="_id")
    })

feeding_report = api.model("feeding_report", {
    'from_date': fields.String(required=True, description="from_date"),
    'to_date': fields.String(required=True, description="to_date")
    })
