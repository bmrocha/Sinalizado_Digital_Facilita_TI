from rest_framework import serializers
from .models import Agency


class AgencySerializer(serializers.ModelSerializer):
    """
    Serializer for Agency model.
    """
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Agency
        fields = [
            'id', 'name', 'code', 'address', 'phone', 'email',
            'orientation', 'hibernation_start', 'hibernation_end',
            'logo', 'logo_url', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
        return None


class AgencyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating agencies.
    """
    class Meta:
        model = Agency
        fields = [
            'name', 'code', 'address', 'phone', 'email',
            'orientation', 'hibernation_start', 'hibernation_end', 'logo'
        ]


class AgencyUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating agencies.
    """
    class Meta:
        model = Agency
        fields = [
            'name', 'code', 'address', 'phone', 'email',
            'orientation', 'hibernation_start', 'hibernation_end',
            'logo', 'is_active'
        ]
