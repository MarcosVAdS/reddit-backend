"""
API V1: Topics Views
"""
###
# Libraries
###
from rest_framework import permissions, viewsets

from helpers.permissions import IsAuthorOrReadOnly
from topics.models import Topic
from .serializers import TopicSerializer


###
# Viewsets
###
class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Topic.objects.all().order_by('id')
    serializer_class = TopicSerializer
    lookup_field = 'url_name'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
