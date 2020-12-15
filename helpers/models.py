"""
Model helper
"""
###
# Libraries
###
import uuid

from django.db import models
from django.utils.translation import ugettext as _


###
# Helpers
###
class TimestampModel(models.Model):
    '''
        Extend this model if you wish to have automatically updated
        created_at and updated_at fields.
    '''

    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, blank=True, auto_now=True)


class TitleBaseModel(models.Model):
    '''
        Extend this model if you wish to have a title field.
    '''

    class Meta:
        abstract = True

    title = models.CharField(max_length=100, null=False, blank=False)


class ContentBaseModel(models.Model):
    '''
        Extend this model if you wish to have a content field.
    '''

    class Meta:
        abstract = True

    content = models.TextField(null=False, blank=False)


class AuthorBaseModel(models.Model):
    '''
        Extend this model if you wish to have author relation with User entity.
    '''

    class Meta:
        abstract = True

    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=False, db_index=True,
                               editable=False)


class UUIDBaseModel(models.Model):
    '''
        Extend this model if you wish to have use an UUID as PK.
    '''

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name=_('uuid'))
