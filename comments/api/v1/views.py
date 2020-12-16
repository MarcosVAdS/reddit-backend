"""
API V1: Comments Views
"""
###
# Libraries
###
from rest_framework import filters, permissions, viewsets

from helpers.permissions import IsAuthorOrReadOnly
from comments.models import Comment
from posts.models import Post
from .serializers import CommentSerializer


###
# Viewsets
###
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'content', 'author__email', 'author__username',
                     'author__first_name', 'author__last_name']

    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['created_at']

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['posts_pk']).order_by('id')

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['posts_pk'])
        serializer.save(author=self.request.user, post=post)
