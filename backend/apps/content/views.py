from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Content
from .serializers import ContentSerializer


class ContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing digital content.
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type', 'agency', 'is_active']

    def get_queryset(self):
        """
        Filter content based on user's agency permissions.
        """
        user = self.request.user
        queryset = Content.objects.select_related('agency')

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
