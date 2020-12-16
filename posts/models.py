"""
Posts Models
"""
###
# Libraries
###
from django.db import models

from topics.models import Topic

from helpers.models import AuthorBaseModel, ContentBaseModel, TimestampModel, TitleBaseModel, \
    UUIDBaseModel
from helpers.s3 import UploadFileTo


###
# Models
###
class Post(UUIDBaseModel, AuthorBaseModel, ContentBaseModel, TimestampModel, TitleBaseModel):
    """
    The equivalent of a Reddit thread, a post belongs to a specific topic and is created by an user.
    """

    # Topic
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE,
                              null=False, db_index=True, to_field='url_name')

    # Image
    image = models.ImageField(null=True, blank=True,
                              upload_to=UploadFileTo('posts-images', 'post'))

    def __str__(self):
        return 'Post({}, {})'.format(self.id, self.topic)
