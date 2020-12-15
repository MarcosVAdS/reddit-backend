"""
Posts admin
"""
###
# Libraries
###
from django.contrib import admin

from helpers.admin import AuthorBaseModelAdmin
from . import models


@admin.register(models.Post)
class PostAdmin(AuthorBaseModelAdmin):
    '''
        Post Admin Model.
    '''
    list_display = ('id', 'author', 'topic', 'created_at', 'updated_at',)
