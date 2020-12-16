"""
API V1: Posts Views
"""
###
# Libraries
###
from rest_framework import filters, permissions, viewsets

from helpers.permissions import IsAuthorOrReadOnly
from posts.models import Post
from topics.models import Topic
from .serializers import PostSerializer


###
# Viewsets
###
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'content', 'author__email', 'author__username',
                     'author__first_name', 'author__last_name']

    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['created_at']

    def get_queryset(self):
        return Post.objects.filter(topic=self.kwargs['topics_url_name'])

    def perform_create(self, serializer):
        topic = Topic.objects.get(url_name=self.kwargs['topics_url_name'])
        serializer.save(author=self.request.user, topic=topic)
