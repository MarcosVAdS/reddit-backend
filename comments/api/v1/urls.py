"""
API V1: Comments Urls
"""
###
# Libraries
###
from django.conf.urls import include, url
from rest_framework_nested import routers

from .views import CommentViewSet

from posts.api.v1.urls import topics_router

###
# Routers
###
""" Posts router """
posts_router = routers.NestedSimpleRouter(topics_router, r'posts', lookup='posts')
posts_router.register(r'comments', CommentViewSet, basename='topic-post-comment')

###
# URLs
###
urlpatterns = [
    url(r'', include(posts_router.urls)),
]
