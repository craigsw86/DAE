from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegulationUpdateViewSet, ChecklistItemViewSet, ComplianceReportView, checklist_view, compliance_report_view

router = DefaultRouter()
router.register(r'regulations', RegulationUpdateViewSet, basename='regulationupdate')
router.register(r'checklist', ChecklistItemViewSet, basename='checklistitem')

urlpatterns = [
    path('checklist-page/', checklist_view, name='checklist_page'),
    path('compliance-report/', compliance_report_view, name='compliance_report_page'),
    path('api/', include(router.urls)),
    path('api/report/', ComplianceReportView.as_view(), name='compliance-report'),
]

urlpatterns += router.urls