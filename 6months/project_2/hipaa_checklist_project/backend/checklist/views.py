from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Case, When, FloatField
from django.db.models.functions import Cast
from .models import ChecklistItem, RegulationUpdate
from .serializers import ChecklistItemSerializer, RegulationUpdateSerializer

class ChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # User-specific filtering (NIST AC-2: Access control)
        return ChecklistItem.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Audit logged automatically
        serializer.save()

class UpdatesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegulationUpdate.objects.all()
    serializer_class = RegulationUpdateSerializer
    permission_classes = [IsAuthenticated]

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Raw SQL for efficiency (mitigate injection with params)
        user_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.username,
                    COUNT(ci.id) AS total_items,
                    SUM(CASE WHEN ci.completed THEN 1 ELSE 0 END) AS completed_items,
                    (SUM(CASE WHEN ci.completed THEN 1 ELSE 0 END) * 100.0 / COUNT(ci.id)) AS completion_percentage
                FROM checklist_checklistitem ci
                JOIN auth_user u ON ci.user_id = u.id
                WHERE ci.user_id = %s
                GROUP BY u.username
            """, [user_id])
            row = cursor.fetchone()

        return Response({
            'username': row[0],
            'total_items': row[1],
            'completed_items': row[2],
            'completion_percentage': row[3]
        })