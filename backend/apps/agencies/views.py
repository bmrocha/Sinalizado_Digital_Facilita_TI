from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Agency
from .serializers import AgencySerializer, AgencyCreateSerializer, AgencyUpdateSerializer


class AgencyListCreateView(generics.ListCreateAPIView):
    """
    List all agencies or create a new agency.
    """
    queryset = Agency.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['orientation', 'is_active']
    search_fields = ['name', 'code', 'email']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AgencyCreateSerializer
        return AgencySerializer

    def get_queryset(self):
        queryset = Agency.objects.all()
        # Filter by user's agency if not admin
        if self.request.user.role != 'admin':
            queryset = queryset.filter(id=self.request.user.agency.id)
        return queryset


class AgencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an agency instance.
    """
    queryset = Agency.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AgencyUpdateSerializer
        return AgencySerializer

    def get_queryset(self):
        queryset = Agency.objects.all()
        # Users can only access their own agency unless they are admin
        if self.request.user.role != 'admin':
            queryset = queryset.filter(id=self.request.user.agency.id)
        return queryset
