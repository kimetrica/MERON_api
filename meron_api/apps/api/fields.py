"""Module that contains Base64ImageField and possibly other custom serializer fields."""
import logging
import uuid
from base64 import b64decode
from binascii import Error as B64DecodeError
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image
from rest_framework import serializers

logger = logging.getLogger(__name__)


class Base64ImageField(serializers.ImageField):
    """A Django REST framework field for handling image-uploads through raw post data.

    This serializer is adopted from https://stackoverflow.com/a/28036805/204706
    An alternative is https://github.com/Hipo/drf-extra-fields, however we should be able to POST both
    multipart/form-data and JSON, the drf-extra-fields serializer only works with base64.
    Another alternative is https://bitbucket.org/levit_scs/drf_base64. This package works with both multipart/form-data
    requests and JSON containing base64 encoded data. However, it expects the base64 string to be HTML-compatible, e.g.
    `data:image/jpeg;base64,R0lGODlh3ADcAPeA[...]`. This requires the clients to specify the correct format in the
    header. The field defined here allows to just include the base64 string without any special header. It uses PIL to
    determine the image format. The `imghdr` package from the standard library was tried but it failed to detect the
    format of a valid JPEG file in our tests.
    """

    def get_file_extension(self, file_name, decoded_file):
        """Use PIL to detect the image format."""
        # The image file has be opened again after img.verify() is used:
        # http://pillow.readthedocs.io/en/4.2.x/reference/Image.html#PIL.Image.Image.verify
        img = Image.open(decoded_file)
        return img.format.lower()

    def to_internal_value(self, data):
        """Check if we are dealing with a base64 encoded file.

        If yes, this is converted to a regular file and then passed to the `to_internal_value` method of the
        baseclass.
        When the `file` payload is not a base64 encoded string, it is passed to the base class as is.
        """
        # Check if this is an image file. If not, we might be dealing with a base64 encoded image. We could also use
        # content negotation to check whether we are dealing with `application/json` or `multipart/form-data`, but it
        # is nicer to keep this generic, so we could in theory also support other content types.
        if isinstance(data, str):
            # Try to b64decode the file. Return validation error if it fails.
            try:
                decoded_string = b64decode(data)
                decoded_file = BytesIO(decoded_string)
                img = Image.open(decoded_file)
                img.verify()
            except (OSError, B64DecodeError):
                logger.exception('No valid image file could be decoded')
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = f'{file_name}.{file_extension}'
            logger.info('Generated filename for base64 encoded file: %s', complete_file_name)

            data = ContentFile(decoded_string, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)
