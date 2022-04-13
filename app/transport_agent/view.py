from flask import request
from flask_restplus import Resource, Namespace
import app.transport_agent.model as transport_agent_model
import app.transport_agent.serializers as transport_agent_serializers
from app import app, bcrypt
import app.Common.serializers as common_serializers
import app.Common.helpers as common_helpers
from datetime import  datetime
import traceback
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity
from bson import json_util
from bson.objectid import ObjectId


transport_agent = Namespace('transport_agent', description='transport agent api')


@transport_agent.route('')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """

    @transport_agent.expect(transport_agent_serializers.transport_agent, validate=True)
    @transport_agent.response(200, app.config["SUCCESS_MESSAGE_200"], transport_agent_serializers.transport_agent)
    @transport_agent.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @transport_agent.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @transport_agent.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @transport_agent.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @transport_agent.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @transport_agent.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @transport_agent.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @transport_agent.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
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
            post_data['_id'] = str(ObjectId())
            post_data['active'] = 1
            user_item = transport_agent_model.RegisterCurb()
            user_item = user_item.insert_data(post_data)

            more_info = "Successfully inserted transport_agent data"
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


@transport_agent.route('/profile')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """
    @transport_agent.expect(transport_agent_serializers.profile, validate=True)
    @transport_agent.response(200, app.config["SUCCESS_MESSAGE_200"], transport_agent_serializers.transport_agent)
    @transport_agent.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @transport_agent.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @transport_agent.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @transport_agent.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @transport_agent.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @transport_agent.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @transport_agent.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @transport_agent.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def post(self):
        try:
            post_data = request.get_json()
            
            user_item = transport_agent_model.RegisterCurb()
            user_item = user_item.read_data({"email":post_data.get('email')})
            # user_item = json_util.dumps(user_item)
            if user_item.get('exists'):
                more_info = "Successfully fetched transport_agent profile data"
            else:
                more_info = "No transport_agent profile data fetched"
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
@transport_agent.route('/count')
# @jwt_required
class Login(Resource):
    """
         This class get form data
         @return: success or failure message
     """

    @transport_agent.response(200, app.config["SUCCESS_MESSAGE_200"], transport_agent_serializers.transport_agent)
    @transport_agent.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @transport_agent.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @transport_agent.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @transport_agent.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @transport_agent.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @transport_agent.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @transport_agent.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @transport_agent.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def get(self):
        try:
            # post_data['created_by'] = current_user
            user_item = transport_agent_model.RegisterCurb()
            user_item = user_item.get_count()
            # user_item = json_util.dumps(user_item)

            more_info = "Successfully fetched transport_agent count"
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

@transport_agent.route('/feeding')
# @jwt_required
class Feeding(Resource):
    """
         This class get form data
         @return: success or failure message
     """

    @transport_agent.response(200, app.config["SUCCESS_MESSAGE_200"], transport_agent_serializers.transport_agent)
    @transport_agent.response(301, app.config["FAILURE_MESSAGE_301"], common_serializers.response_api_model)
    @transport_agent.response(400, app.config["FAILURE_MESSAGE_400"], common_serializers.response_api_model)
    @transport_agent.response(401, app.config["FAILURE_MESSAGE_401"], common_serializers.response_api_model)
    @transport_agent.response(403, app.config["FAILURE_MESSAGE_403"], common_serializers.response_api_model)
    @transport_agent.response(404, app.config["FAILURE_MESSAGE_404"], common_serializers.response_api_model)
    @transport_agent.response(409, app.config["FAILURE_MESSAGE_409"], common_serializers.response_api_model)
    @transport_agent.response(422, app.config["FAILURE_MESSAGE_422"], common_serializers.response_api_model)
    @transport_agent.response(500, app.config["FAILURE_MESSAGE_500"], common_serializers.response_api_model)
    def post(self):
        try:
            user_item = transport_agent_model.RegisterCurb()
            user_item = user_item.get_count()
            """
            

            """

            more_info = "Successfully fetched transport_agent count"
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
