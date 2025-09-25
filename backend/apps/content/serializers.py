from rest_framework import serializers
from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(source='agency.name', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'description', 'content_type', 'url', 'file',
            'file_url', 'duration', 'agency', 'agency_name', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def validate(self, data):
        """
        Validate content based on type.
        """
        content_type = data.get('content_type')
        url = data.get('url')
        file = data.get('file')

        if content_type == 'link' and not url:
            raise serializers.ValidationError({'url': 'URL is required for link content.'})
        if content_type in ['image', 'video'] and not file:
            raise serializers.ValidationError({'file': 'File is required for image/video content.'})

        return data
