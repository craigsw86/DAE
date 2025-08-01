
from rest_framework import viewsets
from .models import RegulationUpdate, ChecklistItem
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegulationUpdateViewSet(viewsets.ModelViewSet):
    queryset = RegulationUpdate.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
