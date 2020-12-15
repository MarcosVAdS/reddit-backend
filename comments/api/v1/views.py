"""
API V1: Comments Views
"""
###
# Libraries
###
from rest_framework import permissions, viewsets

from helpers.permissions import IsAuthorOrReadOnly
from comments.models import Comment
from posts.models import Post
from .serializers import CommentSerializer


###
# Viewsets
###
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['posts_pk']).order_by('id')

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['posts_pk'])
        serializer.save(author=self.request.user, post=post)
