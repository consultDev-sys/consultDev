class CustomValidationError(Exception):
    def __init__(self, error):
        self.error_dict = {
            "code": 400,
            "data": None,
            "errors": error,
            "message": error
        }

class EmailExistsError(CustomValidationError):
    pass

class PhoneNumberExistsError(CustomValidationError):
    pass

class PasswordMismatchError(CustomValidationError):
    pass

class EmailNotFoundError(CustomValidationError):
    pass