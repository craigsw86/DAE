from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Regulation, UserChecklist
from .serializers import RegulationSerializer, UserChecklistSerializer
from django.db.models import Count

class RegulationViewSet(viewsets.ModelViewSet):
    queryset = Regulation.objects.all()
    serializer_class = RegulationSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = UserChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChecklist.objects.filter(user=self.request.user)
    
    def report(self, request):
        total = Regulation.objects.count()
        completed = UserChecklist.objects.filter(user=request.user, completed=True).count()
        percentage = (completed / total * 100) if total else 0
        return Response({'total': total, 'completed': completed, 'percentage': percentage})
