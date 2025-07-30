from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegulationUpdateViewSet, ChecklistItemViewSet, ComplianceReportView

router = DefaultRouter()
router.register(r'regulations', RegulationUpdateViewSet)
router.register(r'checklist', ChecklistItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/report/', ComplianceReportView.as_view(), name='compliance-report'),
]
