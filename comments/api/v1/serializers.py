"""
API V1: Comments Serializers
"""
###
# Libraries
###
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from comments.models import Comment
from posts.api.v1.serializers import PostSerializer


###
# Serializers
###
class CommentSerializer(serializers.ModelSerializer):
    author = UserDetailsSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'post', 'created_at', 'updated_at']
