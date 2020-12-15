"""
API V1: Topics Serializers
"""
###
# Libraries
###
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from topics.models import Topic


###
# Serializers
###
class TopicSerializer(serializers.ModelSerializer):
    author = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ['author', 'url_name', 'created_at', 'updated_at']
