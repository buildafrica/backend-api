from rest_framework.response import Response
from rest_framework import status

class responseHelper:

    def __init__(self, description_object):
        self.description_object = description_object

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
        return self.get_api_response(StatusCodes.Invalid_Field, errors=errors, httpStatusCode=status.HTTP_400_BAD_REQUEST)

    def api_server_error(self):
        return self.get_api_response(response_code=0, httpStatusCode=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def api_success(self):
        return self.get_api_response(response_code=1)


class StatusCodes:
    Server_Error = 0
    Success = 1
    Invalid_Field = 2
    Already_Logged_In = 3
    Invalid_Credentials = 4
    Invalid_Activation_Key = 5
    Activation_Key_Expired = 6
    User_Already_Verified = 7
    Does_Not_Exist = 8
    User_with_Email_Exists = 9
    User_with_Username_Exists = 10

StatusCodesDescription = {
    StatusCodes.Server_Error: "A server error occurred",
    StatusCodes.Success:"Success", 
    StatusCodes.Invalid_Field:"Some fields are invalid",  
    StatusCodes.Already_Logged_In:"User is already logged in",  
    StatusCodes.Invalid_Credentials:"Email or Password is incorrect",  
    StatusCodes.Invalid_Activation_Key:"The activation key is invalid",  
    StatusCodes.Activation_Key_Expired:"The activation key has expired.",  
    StatusCodes.User_Already_Verified:"The user is already verified",  
    StatusCodes.Does_Not_Exist:"No such user in the system",  
    StatusCodes.User_with_Email_Exists:"A user with this email already exists",  
    StatusCodes.User_with_Username_Exists: "A user with this username already exists",
}

ResponseHelper = responseHelper(StatusCodesDescription)