from function.domain.api_model import ResponseObject, ErrorResponseObject


class ResponseMessage:

    @staticmethod
    def resp_200(message: str, type: str, category: str, id: str):
        return ResponseObject(
            statusCode=200,
            id=id,
            type=type,
            category=category,
            message=message
        )

    @staticmethod
    def resp_400(message: str, type: str, category: str, id: str):
        return ErrorResponseObject(
            statusCode=400,
            id=id,
            type=type,
            category=category,
            message=message
        )
