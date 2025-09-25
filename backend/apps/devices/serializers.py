from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    agency_name = serializers.CharField(source='agency.name', read_only=True)
    current_content = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'agency', 'agency_name', 'ip_address', 'mac_address',
            'orientation', 'status', 'last_seen', 'version', 'is_active',
            'current_content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_seen']

    def get_current_content(self, obj):
        content = obj.get_current_content()
        if content:
            return {
                'id': content.id,
                'title': content.title,
                'type': content.content_type,
                'url': content.get_content_url(),
                'duration': content.duration
            }
        return None

    def validate_ip_address(self, value):
        """
        Validate unique IP per agency.
        """
        agency = self.initial_data.get('agency')
        if agency:
            queryset = Device.objects.filter(agency=agency, ip_address=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("IP address already exists for this agency.")
        return value
