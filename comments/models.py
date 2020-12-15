"""
Comments Models
"""
###
# Libraries
###
from django.db import models

from posts.models import Post
from helpers.models import AuthorBaseModel, ContentBaseModel, TimestampModel, TitleBaseModel, \
    UUIDBaseModel
from helpers.s3 import UploadFileTo


###
# Models
###
class Comment(UUIDBaseModel, AuthorBaseModel, ContentBaseModel, TimestampModel, TitleBaseModel):
    """
    The equivalent of a comment, a comment belongs to a specific post
    (which belongs to a specific topic) and is created by an user.
    """

    # Post
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE,
                             null=False, db_index=True)

    # Image
    image = models.ImageField(null=True, blank=True,
                              upload_to=UploadFileTo('posts-images', 'post'))
