from django.urls import path
from .views import AgencyListCreateView, AgencyDetailView

app_name = 'agencies'

urlpatterns = [
    path('agencies/', AgencyListCreateView.as_view(), name='agency_list_create'),
    path('agencies/<int:pk>/', AgencyDetailView.as_view(), name='agency_detail'),
]
