"""
API V1: Posts Urls
"""
###
# Libraries
###
from django.conf.urls import include, url
from rest_framework_nested import routers

from .views import PostViewSet

from topics.api.v1.urls import main_router

###
# Routers
###
""" Topics router """
topics_router = routers.NestedSimpleRouter(main_router, r'topics', lookup='topics')
topics_router.register(r'posts', PostViewSet, basename='topic-post')

###
# URLs
###
urlpatterns = [
    url(r'', include(topics_router.urls)),
]
