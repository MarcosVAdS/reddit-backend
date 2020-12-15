"""
Admin helper
"""
###
# Libraries
###
from django.contrib import admin


###
# Helpers
###
class AuthorBaseModelAdmin(admin.ModelAdmin):
    '''
        Extend this model if you wish to autofill the author field in admin.
    '''

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
