from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Raspberry Pi devices.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['agency', 'status', 'is_active']

    def get_queryset(self):
        """
        Filter devices based on user's agency permissions.
        """
        user = self.request.user
        queryset = Device.objects.select_related('agency')

        if user.role in ['admin']:
            return queryset
        elif user.role == 'gestor':
            return queryset.filter(agency=user.agency)
        else:
            return queryset.none()

    def perform_create(self, serializer):
        """
        Set the agency based on the user's agency for gestores.
        """
        user = self.request.user
        if user.role == 'gestor' and hasattr(user, 'agency'):
            serializer.save(agency=user.agency)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def heartbeat(self, request, pk=None):
        """
        Update device status and last seen time.
        """
        device = self.get_object()
        status_value = request.data.get('status', 'online')
        version = request.data.get('version')

        device.update_status(status_value, version)

        serializer = self.get_serializer(device)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def content(self, request, pk=None):
        """
        Get current content for the device.
        """
        device = self.get_object()
        content = device.get_current_content()

        if content:
            data = {
                'id': content.id,
                'title': content.title,
                'type': content.content_type,
                'url': content.get_content_url(),
                'duration': content.duration
            }
            return Response(data)
        else:
            return Response(
                {'message': 'No content scheduled for current time'},
                status=status.HTTP_204_NO_CONTENT
            )
