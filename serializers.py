from rest_framework import serializers

from . import models


class FlatSerializer(serializers.ModelSerializer):
    """

    """
    gender = serializers.CharField(source='get_gender')

    class Meta:
        model = models.Flat
        fields = ['message', 'user_fb_name', 'user_fb_id', 'publish_at', 'phone_number', 'image', 'furnishing_type',
                  'is_available', 'like_count', 'gender']

