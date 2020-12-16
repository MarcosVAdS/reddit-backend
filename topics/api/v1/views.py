"""
API V1: Topics Views
"""
###
# Libraries
###
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from helpers.permissions import IsAuthorOrReadOnly
from topics.models import Topic
from .serializers import TopicSerializer


###
# Viewsets
###
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = ['name', 'title', 'description', 'author__email', 'author__username',
                     'author__first_name', 'author__last_name']
    filterset_fields = ['name', 'title', 'author', 'created_at', 'updated_at']

    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['created_at']

    lookup_field = 'url_name'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
