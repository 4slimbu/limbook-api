class ImageUploadError(Exception):
    """ ImageError Exception

    A standardized way to communicate Image Upload failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
