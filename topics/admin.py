"""
Topics admin
"""
###
# Libraries
###
from django.contrib import admin

from helpers.admin import AuthorBaseModelAdmin
from . import models


@admin.register(models.Topic)
class TopicAdmin(AuthorBaseModelAdmin):
    '''
        Topic Admin Model.
    '''
    list_display = ('id', 'author', 'name', 'url_name', 'created_at', 'updated_at',)
