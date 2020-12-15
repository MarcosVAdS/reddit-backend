"""
Comments admin
"""
###
# Libraries
###
from django.contrib import admin

from helpers.admin import AuthorBaseModelAdmin
from . import models


@admin.register(models.Comment)
class CommentAdmin(AuthorBaseModelAdmin):
    '''
        Comment Admin Model.
    '''
    list_display = ('id', 'author', 'post', 'created_at', 'updated_at',)
