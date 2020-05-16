class ValidationError(Exception):
    """ Validation Exception

    A standardized way to communicate Image Upload failure modes
    """

    def __init__(self, errors):
        self.error = {
            "code": "validation_error",
            "description": "One or more field validation failed",
            "errors": errors
        }
        self.status_code = 422
