from rest_framework import serializers

from media.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'email',
            'date',
            'location',
            'path'
        )
