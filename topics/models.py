"""
Topics Models
"""
###
# Libraries
###
from django.db import models
from django.utils.text import slugify

from helpers.models import AuthorBaseModel, TimestampModel, TitleBaseModel, UUIDBaseModel
from helpers.s3 import UploadFileTo


###
# Models
###
class Topic(UUIDBaseModel, AuthorBaseModel, TimestampModel, TitleBaseModel):
    """
    The equivalent of a sub-reddit.
    """

    # Name
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    # URL Name: the name we want to use to reach it through the browser
    url_name = models.SlugField(max_length=100, null=False, blank=False,
                                unique=True, editable=False)

    # Description
    description = models.CharField(max_length=280, null=False, blank=True)

    # Image
    image = models.ImageField(null=True, blank=True,
                              upload_to=UploadFileTo('topics-images', 'topic'))

    def save(self, *args, **kwargs):
        self.url_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Topic({}, {})'.format(self.id, self.url_name)
