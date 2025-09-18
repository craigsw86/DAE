from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegulationUpdateViewSet, ChecklistItemViewSet, ComplianceReportView, checklist_view, compliance_report_view, AuditLogView, UserProfileView, ChecklistExportCSV, ChecklistExportPDF, ReportTrendsView
from .public_views import health_check, api_info, public_checklist_stats
from .security_views import security_report, run_security_scan

router = DefaultRouter()
router.register(r'regulations', RegulationUpdateViewSet, basename='regulationupdate')
router.register(r'checklist', ChecklistItemViewSet, basename='checklistitem')

urlpatterns = [
    path('checklist-page/', checklist_view, name='checklist_page'),
    path('compliance-report/', compliance_report_view, name='compliance_report_page'),
    path('api/', include(router.urls)),
    path('api/report/', ComplianceReportView.as_view(), name='compliance-report'),
    path('api/auditlog/<str:model_name>/<int:object_id>/', AuditLogView.as_view(), name='auditlog-api'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/checklist/export/csv/', ChecklistExportCSV.as_view(), name='checklist-export-csv'),
    path('api/checklist/export/pdf/', ChecklistExportPDF.as_view(), name='checklist-export-pdf'),
    path('api/report/trends/', ReportTrendsView.as_view(), name='report-trends'),
    # Security endpoints
    path('api/security/report/', security_report, name='security-report'),
    path('api/security/scan/', run_security_scan, name='security-scan'),
    # Public endpoints (no authentication required)
    path('api/health/', health_check, name='health-check'),
    path('api/info/', api_info, name='api-info'),
    path('api/stats/', public_checklist_stats, name='public-stats'),
]

urlpatterns += router.urls