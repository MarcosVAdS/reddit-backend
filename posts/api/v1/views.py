"""
API V1: Posts Views
"""
###
# Libraries
###
from rest_framework import permissions, viewsets

from helpers.permissions import IsAuthorOrReadOnly
from posts.models import Post
from topics.models import Topic
from .serializers import PostSerializer


###
# Viewsets
###
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(topic=self.kwargs['topics_url_name']).order_by('id')

    def perform_create(self, serializer):
        topic = Topic.objects.get(url_name=self.kwargs['topics_url_name'])
        serializer.save(author=self.request.user, topic=topic)
