from django.urls import path
from .views import (
    FormListCreateAPIView,
    FormDetailAPIView,
    FieldListCreateAPIView,
    FieldDetailAPIView,
)

urlpatterns = [
    # Form endpoints
    path('forms/', FormListCreateAPIView.as_view(), name='form-list-create'),
    path('forms/<uuid:pk>/', FormDetailAPIView.as_view(), name='form-detail'),

    # Field endpoints
    path('fields/', FieldListCreateAPIView.as_view(), name='field-list-create'),
    path('fields/<uuid:pk>/', FieldDetailAPIView.as_view(), name='field-detail'),
]
