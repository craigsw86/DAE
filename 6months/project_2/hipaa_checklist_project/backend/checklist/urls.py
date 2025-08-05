from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegulationUpdateViewSet, ChecklistItemViewSet, ComplianceReportView

router = DefaultRouter()
router.register(r'regulations', RegulationUpdateViewSet, basename='regulationupdate')
router.register(r'checklist', ChecklistItemViewSet, basename='checklistitem')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/report/', ComplianceReportView.as_view(), name='compliance-report'),
]

urlpatterns += router.urls