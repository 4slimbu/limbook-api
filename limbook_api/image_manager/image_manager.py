import io
import os
import secrets

from PIL import Image as PImage
from flask import current_app, abort
from werkzeug.utils import secure_filename

from limbook_api.errors import ImageUploadError


def generate_img_in_bytes(width=500, height=500):
    """ Generate image in bytes

    Useful for image upload testing but can be modified to
    make it suitable for creating placeholder as well.
    """
    # create one by one pixel image
    one_by_one_image = PImage.new('RGB', (width, height), 'white')

    # write to binary
    byte_img = io.BytesIO()
    one_by_one_image.save(byte_img, format='JPEG')

    return byte_img.getvalue()


def generate_unique_img_dir():
    image_dir_name = secrets.token_hex(16)
    image_dir_path = os.path.join(
        current_app.root_path,
        current_app.config.get('IMG_UPLOAD_DIR'),
        image_dir_name
    )
    os.makedirs(image_dir_path, exist_ok=True)

    return image_dir_path


def create_img_set(image_file):
    """ Create different sizes images

    It currently uses Pillow to achieve the feat.
    """
    # TODO: This can be simplified by using flask-uploads
    #     https://pythonhosted.org/Flask-Uploads/
    sizes = current_app.config.get('IMG_SIZES')
    image_set = {}
    image_fullname = secure_filename(image_file.filename)

    image_dir_path = generate_unique_img_dir()
    image_name, image_ext = os.path.splitext(image_fullname)

    if image_ext not in current_app.config.get('ALLOWED_EXTENSIONS'):
        raise ImageUploadError({
            'code': 'file_extension_not_allowed',
            'description': 'Only jpg, jpeg and png are supported'
        }, 400)

    try:
        # Save image set
        i = PImage.open(image_file)
        for thumb, size in sizes.items():
            i = i.copy()
            i.thumbnail(size, PImage.LANCZOS)
            i_path = ''.join(
                [
                    image_dir_path, '/', image_name, '-', thumb, '-',
                    str(size[0]), 'x', str(size[1]), image_ext
                ]
            )
            i.save(i_path, optimize=True, quality=95)
            image_set[thumb] = i_path

        return image_set
    except Exception as e:
        raise ImageUploadError({
            'code': 'image_upload_error',
            'description': 'Unable to save Image set'
        }, 400)


def delete_image_set(image):
    url_set = image.format().get('url')
    for value in url_set.values():
        if os.path.isfile(value):
            os.remove(value)
