"""
reddit-backend URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib import admin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.views.generic import RedirectView


from helpers.health_check_view import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="REDDIT API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
###
# URLs
###
urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Health Check
    url(r'health-check/$', health_check, name='health_check'),

    # Applications
    url(r'^', include('accounts.urls')),
    url(r'^', include('topics.urls')),
    url(r'^', include('posts.urls')),
    url(r'^', include('comments.urls')),

    # Swagger
    re_path(
        r"^api/v1(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/v1/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", RedirectView.as_view(url="/api/v1")),
]
