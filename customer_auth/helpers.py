def get_error_string_from_serializer_error_object(error_dict_object):
    if error_dict_object:
        # Handle non-field errors
        if 'non_field_errors' in error_dict_object:
            return error_dict_object['non_field_errors'][0]

        # Check if it's a field-specific error
        for field, errors in error_dict_object.items():
            if isinstance(errors, list) and errors:
                if "code" in errors[0] and errors[0].code == "required":
                    return f"{field.capitalize()} is required"
                return f"{field.capitalize()}: {errors[0]}"

    # Default error message
    return ("Can't Perform Action Right Now. "
            "Please Try Again Later. If problem persists please create a support "
            "ticket to reach us.")