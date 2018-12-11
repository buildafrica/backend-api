from Authorization.responseHelper import (responseHelper, BaseStatusCodes, BaseStatusCodesDescription, 
                                        get_api_response, get_api_server_error, get_api_success, get_400_error)

class StatusCodes(BaseStatusCodes):
    Invalid_Params_Or_Unauthenticated = 3

class StatusCodesDescription(BaseStatusCodesDescription):
    descriptors = {
        StatusCodes.Invalid_Params_Or_Unauthenticated: "Invalid Id param or User unauthenticated"
    }

    def __getitem__(self, key):
        try:
            return self.descriptors[key]
        except KeyError as e:
            return BaseStatusCodesDescription.__dict__['desc'][key]


ResponseHelper = responseHelper(StatusCodes, StatusCodesDescription)