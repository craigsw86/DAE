"""
Public API views that don't require authentication
For testing and public access
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'HIPAA Checklist API is running',
        'version': '1.0.0'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'HIPAA Checklist API',
        'version': '1.0.0',
        'description': 'HIPAA compliance checklist management system',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'checklist': '/api/checklist/ (requires auth)',
            'regulations': '/api/regulations/ (requires auth)',
            'admin': '/admin/',
            'token': '/api/token/'
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_checklist_stats(request):
    """Public checklist statistics (no sensitive data)"""
    try:
        from .models import ChecklistItem
        total_items = ChecklistItem.objects.count()
        completed_items = ChecklistItem.objects.filter(completed=True).count()
        
        return Response({
            'total_items': total_items,
            'completed_items': completed_items,
            'completion_rate': round((completed_items / total_items * 100) if total_items > 0 else 0, 2)
        })
    except Exception as e:
        return Response({
            'error': 'Unable to retrieve statistics',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

