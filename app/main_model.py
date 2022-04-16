from app import app
import app.Common.helpers as common_helpers
import traceback
from app import mongo
from pymongo import ReturnDocument


class RegisterCurb:
    """
         This class insert data
         @author:
         @return: success or failure message
     """
    def __init__(self):
        # assigning collection name here
        self.img_db_col = mongo.db.img_db
        self.extract_db_col = mongo.db.extracted_data

    def insert_extracted_data(self, query):
        try:
            registered_email = self.extract_db_col.insert_one(query)
      
        except Exception as e:
            more_info = "Unable to Inserted data : Exception occurred - " + traceback.format_exc()
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)

    def insert_data(self, query):
        try:
            registered_email = self.img_db_col.insert_one(query)
      
        except Exception as e:
            more_info = "Unable to Inserted data : Exception occurred - " + traceback.format_exc()
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)

    def read_data(self, query):
        try:
            print(f"read data query is: {query}")
            result_data = self.img_db_col.find_one(query)
            print(result_data)
            if result_data:
                return {"exists": True, "data": result_data}
            return {"exists": False, "data": result_data}

        except Exception as e:
            more_info = "Unable to fetch data : Exception occurred - " + traceback.format_exc()
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)

    # read all data in the img_db collection
    def read_all_data(self):
        try:
            result_data = self.img_db_col.find()
            print(result_data)
            if result_data:
                return {"exists": True, "data": list(result_data)}
            return {"exists": False, "data": result_data}

        except Exception as e:
            more_info = "Unable to fetch data : Exception occurred - " + traceback.format_exc()
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)


    def find_modify(self, query, update):
        try:
            result_data = self.img_db_col.find_one_and_update(query,{'$set':update}, return_document = ReturnDocument.AFTER)
            print(result_data)
            if result_data:
                return {"exists": True, "data": result_data}
            return {"exists": False, "data": result_data}

        except Exception as e:
            more_info = "Unable to fetch data : Exception occurred - " + traceback.format_exc()
            return common_helpers.response('failed',
                                           app.config["FAILURE_MESSAGE_500"],
                                           more_info, [], 500)

