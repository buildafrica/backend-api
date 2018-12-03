from rest_framework.response import Response
from rest_framework import status

class responseHelper:

    def __init__(self, status_codes, description_object):
        self.status_codes = status_codes
        self.description_object = description_object()

    def get_api_response(self, response_code=1, data={}, errors={}, httpStatusCode = 200):
        '''Returns a response object'''
        try:
            self.description_object[response_code]
        except Exception as e:
            # Log error.
            return self.api_server_error()

        response_data = {"status": response_code, "description": self.description_object[response_code], "data": data, "errors": errors}   
        return Response(data=response_data, status=httpStatusCode)

    # Helper Methods

    def api_400_error(self, errors):
        return self.get_api_response(self.status_codes.Invalid_Field, errors=errors, httpStatusCode=status.HTTP_400_BAD_REQUEST)

    def api_server_error(self):
        return self.get_api_response(response_code=0, httpStatusCode=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def api_success(self):
        return self.get_api_response(response_code=1)


class BaseStatusCodes:
    Server_Error = 0
    Success = 1
    Invalid_Field = 2

class BaseStatusCodesDescription:
    descriptors = {
        BaseStatusCodes.Server_Error: "A server error occurred",
        BaseStatusCodes.Success:"Success", 
        BaseStatusCodes.Invalid_Field:"Some fields are invalid"
    }

    def __getitem__(self, key):
        return self.descriptors[key]

class StatusCodes(BaseStatusCodes):
    Invalid_Field = 2
    Already_Logged_In = 3
    Invalid_Credentials = 4
    Invalid_Activation_Key = 5
    Activation_Key_Expired = 6
    User_Already_Verified = 7
    Does_Not_Exist = 8
    User_with_Email_Exists = 9
    User_with_Username_Exists = 10
    User_Unaunthenticated = 11

class StatusCodesDescription(BaseStatusCodesDescription):
    descriptors = {  
        StatusCodes.Already_Logged_In:"User is already logged in",  
        StatusCodes.Invalid_Credentials:"Email or Password is incorrect",  
        StatusCodes.Invalid_Activation_Key:"The activation key is invalid",  
        StatusCodes.Activation_Key_Expired:"The activation key has expired.",  
        StatusCodes.User_Already_Verified:"The user is already verified",  
        StatusCodes.Does_Not_Exist:"No such user in the system",  
        StatusCodes.User_with_Email_Exists:"A user with this email already exists",  
        StatusCodes.User_with_Username_Exists: "A user with this username already exists",
        StatusCodes.User_Unaunthenticated: "User needs to be logged in",
    }

    def __getitem__(self, key):
        msg = super().__getitem__(key)

        if msg is None:
            msg = self.descriptors[key]
            if msg is None:
                raise IndexError("Invalid Status Code")
            

ResponseHelper = responseHelper(StatusCodes, StatusCodesDescription)
get_api_response = ResponseHelper.get_api_response
get_api_server_error = ResponseHelper.api_server_error
get_api_success = ResponseHelper.api_success
get_400_error = ResponseHelper.api_400_error