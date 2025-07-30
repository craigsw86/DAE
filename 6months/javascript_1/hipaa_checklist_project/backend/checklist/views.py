from django.shortcuts import render
from rest_framework import viewsets
from .models import RegulationUpdate, ChecklistItem
from .serializers import RegulationUpdateSerializer, ChecklistItemSerializer

# Create your views here.

class RegulationUpdateViewSet(viewsets.ModelViewSet):
    queryset = RegulationUpdate.objects.all().order_by('-created_at')
    serializer_class = RegulationUpdateSerializer

class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.all().order_by('-last_updated')
    serializer_class = ChecklistItemSerializer
