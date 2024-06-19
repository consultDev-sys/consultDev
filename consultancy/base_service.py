from rest_framework import status

class BaseService():
    def __init__(self):
        self.response = {
            "code": "",
            "data": {},
            "errors": {},
            "message": ""
        }

    @staticmethod
    def send_response(code=status.HTTP_200_OK, data="", errors="", message=""):
        return {
            "code": code,
            "data": data,
            "errors": errors,
            "message": message
        }
