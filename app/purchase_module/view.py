from flask import request
from flask_restplus import Resource, Namespace, reqparse
import app.purchase_module.model as purchase_module_model
import app.purchase_module.serializers as purchase_module_serializers
from app import app, bcrypt
import app.Common.serializers as common_serializers
import app.Common.helpers as common_helpers
from datetime import  datetime
import traceback
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
import werkzeug
import os
from utils.helpers import get_image_text


comp_conf = {
    "company_name": "488,46,804,80",
    "phone_no": "284,107,1004,140",
    "gst_no": "560,138,803,168",
    "customer_name": "54,171,576,201",
    "bill_no": "940,172,1218,195",
    "bill_date": "939,193,1174,219",
    "description": "53,225,1260,521",
    "total_amount_in_words": "43,647,585,694",
    "net_amount": "899,745,1247,783"

}

purchase_cal = Namespace('purchase_module', description='purchase call api')

# create an api to upload image and store in uploads folder
@purchase_cal.route('/upload_image')
class UploadImage(Resource):
    # @purchase_cal.expect(common_serializers.upload_model)
    def post(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
            args = parse.parse_args()
            image_file = args['file']

            file_name = image_file.filename
            file_path = app.config["UPLOAD_IMG_PATH"]
            # create this month folder if not exists
            file_path = os.path.join(file_path, datetime.now().strftime("%Y-%m"))
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_store_path = os.path.join(file_path, file_name)
            image_file.save(file_store_path)

            result = get_image_text(file_store_path, comp_conf)
            
            return result
        except Exception as e:
            print(traceback.format_exc())
            return  traceback.format_exc()

@purchase_cal.route('')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """

    @purchase_cal.expect(purchase_module_serializers.purchase_module, validate=True)
    @purchase_cal.response(200, app.config["SUCCESS_MESSAGE_200"], purchase_module_serializers.purchase_module)
    @purchase_cal.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @purchase_cal.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @purchase_cal.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @purchase_cal.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @purchase_cal.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @purchase_cal.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @purchase_cal.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @purchase_cal.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def post(self):
        try:
            if not (request.content_type == 'application/json'):
                return common_helpers.response('failed',
                                               app.config["FAILURE_MESSAGE_400"],
                                               'Content type should be application/json',
                                               [], 400)
            post_data = request.get_json()
            token = post_data.get("token")
            current_user = get_jwt_identity()

            # check user has valid access token 
            post_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            post_data['created_by'] = current_user
            post_data['active'] = 1
            post_data['_id'] = f"PURCHASE{str(ObjectId())}"
            user_item = purchase_module_model.RegisterCurb()
            user_item = user_item.insert_data(post_data)

            more_info = {}
            more_info['purchase_call_status'] = "Successfully inserted purchase data"
            return common_helpers.response('success',
                                           app.config["SUCCESS_MESSAGE_200"],
                                           more_info,
                                           [],
                                           200,
                                           post_data.get('token'))
        except Exception as e:
            e = f"{traceback.format_exc()}"
            more_info = "Unable to Inserted data :Exception occurred - " + str(e)
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)

@purchase_cal.route('/count')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """

    @purchase_cal.response(200, app.config["SUCCESS_MESSAGE_200"], purchase_module_serializers.purchase_module)
    @purchase_cal.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @purchase_cal.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @purchase_cal.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @purchase_cal.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @purchase_cal.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @purchase_cal.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @purchase_cal.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @purchase_cal.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def get(self):
        try:
            # post_data['created_by'] = current_user
            user_item = purchase_module_model.RegisterCurb()
            user_item = user_item.get_count()

            more_info = "Successfully fetched purchase count"
            return common_helpers.response('success',
                                           app.config["SUCCESS_MESSAGE_200"],
                                           more_info,
                                           user_item,
                                           200)
        except Exception as e:
            e = f"{traceback.format_exc()}"
            more_info = "Unable to Inserted data :Exception occurred - " + str(e)
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)


@purchase_cal.route('/approve')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """

    @purchase_cal.expect(purchase_module_serializers.approval, validate=True)
    @purchase_cal.response(200, app.config["SUCCESS_MESSAGE_200"], purchase_module_serializers.purchase_module)
    @purchase_cal.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @purchase_cal.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @purchase_cal.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @purchase_cal.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @purchase_cal.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @purchase_cal.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @purchase_cal.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @purchase_cal.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def put(self):
        try:
            if not (request.content_type == 'application/json'):
                return common_helpers.response('failed',
                                               app.config["FAILURE_MESSAGE_400"],
                                               'Content type should be application/json',
                                               [], 400)
            post_data = request.get_json()
            token = post_data.get("token")
            current_user = get_jwt_identity()
            # check user has valid access token

            post_data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            post_data['updated_by'] = current_user
            id_number = post_data.get("_id")
            post_data['active'] = 1
            user_item = purchase_module_model.RegisterCurb()
            user_item = user_item.find_modify({'_id': id_number}, post_data)

            more_info = "Successfully approved"
            return common_helpers.response('success',
                                           app.config["SUCCESS_MESSAGE_200"],
                                           more_info,
                                           [],
                                           200,
                                           post_data.get('token'))
        except Exception as e:
            e = f"{traceback.format_exc()}"
            more_info = "Unable to Inserted data :Exception occurred - " + str(e)
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)


@purchase_cal.route('/feeding_report')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """
    @purchase_cal.expect(purchase_module_serializers.feeding_report, validate=True)
    @purchase_cal.response(200, app.config["SUCCESS_MESSAGE_200"], purchase_module_serializers.feeding_report)
    @purchase_cal.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @purchase_cal.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @purchase_cal.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @purchase_cal.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @purchase_cal.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @purchase_cal.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @purchase_cal.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @purchase_cal.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def post(self):
        try:
            post_data = request.get_json()
            from_date = post_data.get("from_date")
            to_date = post_data.get("to_date")
            user_item = purchase_module_model.RegisterCurb()
            query = {
                "created_at":{
                    "$gt": f"{from_date}",
                    "$lt": f"{to_date}" 
                    }
                }

            user_item = user_item.get_feeding_info(query)
            
            more_info = "Successfully fetched purchase call feeding report"
            return common_helpers.response('success',
                                           app.config["SUCCESS_MESSAGE_200"],
                                           more_info,
                                           user_item,
                                           200)
        except Exception as e:
            e = f"{traceback.format_exc()}"
            more_info = "Unable to fetch data :Exception occurred - " + str(e)
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)
