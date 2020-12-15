"""
API V1: Posts Serializers
"""
###
# Libraries
###
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from posts.models import Post
from topics.api.v1.serializers import TopicSerializer


###
# Serializers
###
class PostSerializer(serializers.ModelSerializer):
    author = UserDetailsSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'topic', 'created_at', 'updated_at']
