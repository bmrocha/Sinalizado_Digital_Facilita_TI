from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing content schedules.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content', 'is_active', 'content__agency']

    def get_queryset(self):
        """
        Filter schedules based on user's agency permissions.
        """
        user = self.request.user
        queryset = Schedule.objects.select_related('content', 'content__agency')

        if user.role in ['admin']:
            return queryset
        elif user.role == 'gestor':
            return queryset.filter(content__agency=user.agency)
        else:
            return queryset.none()

    def perform_create(self, serializer):
        """
        Set the content's agency based on the user's agency.
        """
        user = self.request.user
        if user.role == 'gestor' and hasattr(user, 'agency'):
            content = serializer.validated_data['content']
            if content.agency != user.agency:
                raise permissions.PermissionDenied("Cannot create schedule for content from different agency.")
        serializer.save()

    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get current active schedules.
        """
        from django.utils import timezone
        now = timezone.now()
        current_time = now.time()
        current_day = now.weekday()

        schedules = self.get_queryset().filter(
            is_active=True,
            days_of_week__contains=[current_day],
            start_time__lte=current_time,
            end_time__gte=current_time
        ).order_by('-priority')

        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)
