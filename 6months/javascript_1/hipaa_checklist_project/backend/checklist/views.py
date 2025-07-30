from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RegulationUpdate, ChecklistItem
from .serializers import RegulationUpdateSerializer, ChecklistItemSerializer

# Create your views here.

class RegulationUpdateViewSet(viewsets.ModelViewSet):
    queryset = RegulationUpdate.objects.all().order_by('-created_at')
    serializer_class = RegulationUpdateSerializer
    permission_classes = [IsAuthenticated]

class ChecklistItemViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChecklistItem.objects.filter(user=self.request.user).order_by('-last_updated')

class ComplianceReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total = ChecklistItem.objects.filter(user=user).count()
        completed = ChecklistItem.objects.filter(user=user, completed=True).count()
        percent = (completed / total * 100) if total > 0 else 0
        return Response({
            'user': user.username,
            'total_items': total,
            'completed_items': completed,
            'completion_percentage': round(percent, 2),
        })
