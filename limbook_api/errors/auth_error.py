class AuthError(Exception):
    """ AuthError Exception

    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
