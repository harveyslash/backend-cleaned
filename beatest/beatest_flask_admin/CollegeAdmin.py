import os
import os.path as op

from PIL import Image, ImageOps
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import thumbgen_filename, FileUploadField, \
    ImageUploadInput
from flask_admin.form.rules import BaseRule
from markupsafe import Markup
from wtforms.utils import unset_value
import boto3

from beatest_flask_admin.helpers import BaseAdminView

s3 = boto3.resource('s3')
BUCKET = "beatest-blobs"
BUCKET_PREFIX = "blobs/college_logos/"


# unused
class ImageUploadField(FileUploadField):
    """
        Image upload field.

        Does image validation, thumbnail generation, updating and deleting images.

        Requires PIL (or Pillow) to be installed.
    """
    widget = ImageUploadInput()

    keep_image_formats = ('PNG',)
    """
        If field detects that uploaded image is not in this list, it will save image
        as PNG.
    """

    def __init__(self, label=None, validators=None,
                 base_path=None, relative_path=None,
                 namegen=None, allowed_extensions=None,
                 max_size=None,
                 thumbgen=None, thumbnail_size=None,
                 permission=0o666,
                 url_relative_path=None, endpoint='static',
                 **kwargs):
        # Check if PIL is installed
        if Image is None:
            raise ImportError('PIL library was not found')

        self.max_size = max_size
        self.thumbnail_fn = thumbgen or thumbgen_filename
        self.thumbnail_size = thumbnail_size
        self.endpoint = endpoint
        self.image = None
        self.url_relative_path = url_relative_path

        if not allowed_extensions:
            allowed_extensions = ('gif', 'jpg', 'jpeg', 'png', 'tiff')

        super(ImageUploadField, self).__init__(label, validators,
                                               base_path=base_path,
                                               relative_path=relative_path,
                                               namegen=namegen,
                                               allowed_extensions=allowed_extensions,
                                               permission=permission,
                                               **kwargs)

    def pre_validate(self, form):
        super(ImageUploadField, self).pre_validate(form)

        if self._is_uploaded_file(self.data):
            try:
                self.image = Image.open(self.data)
            except Exception as e:
                from wtforms import ValidationError
                raise ValidationError('Invalid image: %s' % e)

    # Deletion
    def _delete_file(self, filename):
        super(ImageUploadField, self)._delete_file(filename)

        self._delete_thumbnail(filename)

    def _delete_thumbnail(self, filename):
        print("hmm")
        path = self._get_path(self.thumbnail_fn(filename))

        if op.exists(path):
            os.remove(path)

    # Saving
    def _save_file(self, data, filename):
        print("AAAA")
        path = self._get_path(filename)

        if not op.exists(op.dirname(path)):
            os.makedirs(os.path.dirname(path), self.permission | 0o111)

        # Figure out format
        filename, format = self._get_save_format(filename, self.image)

        if self.image and (self.image.format != format or self.max_size):
            if self.max_size:
                image = self._resize(self.image, self.max_size)
            else:
                image = self.image

            self._save_image(image, self._get_path(filename), format)
        else:
            data.seek(0)
            data.save(self._get_path(filename))

        self._save_thumbnail(data, filename, format)

        return filename

    def _save_thumbnail(self, data, filename, format):
        print("here")
        if self.image and self.thumbnail_size:
            path = self._get_path(self.thumbnail_fn(filename))

            self._save_image(self._resize(self.image, self.thumbnail_size),
                             path,
                             format)

    def _resize(self, image, size):
        print("here2")
        (width, height, force) = size

        if image.size[0] > width or image.size[1] > height:
            if force:
                return ImageOps.fit(self.image, (width, height),
                                    Image.ANTIALIAS)
            else:
                thumb = self.image.copy()
                thumb.thumbnail((width, height), Image.ANTIALIAS)
                return thumb

        return image

    def _save_image(self, image, path, format='JPEG'):
        print("here3")
        print(image)
        print(path)
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')

        with open(path, 'wb') as fp:
            image.save(fp, format)

    def _get_save_format(self, filename, image):
        print("here4")
        if image.format not in self.keep_image_formats:
            name, ext = op.splitext(filename)
            filename = '%s.jpg' % name
            return filename, 'JPEG'

        return filename, image.format

    def process(self, formdata, data=unset_value):
        # print(formdata)
        print("HAAAAAAAAAAA")
        super(FileUploadField, self).process(formdata, data)


# unused
class S3ImageUploadField(ImageUploadField):

    def __init__(self, *args, **kwargs):
        super(S3ImageUploadField, self).__init__(*args, **kwargs)

    def pre_validate(self, form):
        self.image = Image.open(self.data)
        print(form.data)

    def _save_thumbnail(self, data, filename, format):
        super()._save_thumbnail(data, filename, format)
        print("-" * 10)
        print(data)
        print(filename)
        path = self._get_path(self.thumbnail_fn(filename))
        print(path)
        s3.Bucket(BUCKET).upload_file(path,
                                      f"blobs/college_logos/{path.split('/')[-1]}")
        print("-" * 10)

    def process(self, formdata, data=unset_value):
        super().process(formdata, data)
        print("processing form data in child")
        # formdata['college_logo'] = "as;ldkfjaslkdfj.png"
        print(data)
        print(formdata)
        print("processing form data in child don1")
        pass


class CollegeImagePreview(BaseRule):
    def __init__(self, attribute):
        super(CollegeImagePreview, self).__init__()
        self.attribute = attribute

    def __call__(self, form, form_opts=None, field_args={}):
        logo = form._obj.college_logo

        return Markup(
                f"<img src='https://beatest.in{logo}'/>")


class CollegeAdmin(BaseAdminView):
    form_create_rules = ('college_name',
    'college_logo',
    CollegeImagePreview('college_logo')
    )

    # form_overrides = {
    #     'college_logo': S3ImageUploadField
    # }
    # form_args = {
    #     'college_logo': {
    #         'label': 'college_logo',
    #         'base_path': "college_logos",
    #         'allow_overwrite': True,
    #         'thumbnail_size': (1024, 1024, False)
    #     }
    # }

    form_edit_rules = form_create_rules
