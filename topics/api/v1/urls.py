"""
API V1: Topics Urls
"""
###
# Libraries
###
from django.conf.urls import include, url
from rest_framework_nested import routers

from .views import TopicViewSet

###
# Routers
###
""" Main router """
main_router = routers.SimpleRouter()
main_router.register(r'topics', TopicViewSet)


###
# URLs
###
urlpatterns = [
    url(r'', include(main_router.urls)),
]
