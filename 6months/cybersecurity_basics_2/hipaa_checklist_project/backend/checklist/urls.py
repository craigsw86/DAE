from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ChecklistViewSet, UpdatesViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'checklist', ChecklistViewSet)
router.register(r'updates', UpdatesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/', ReportViewSet.as_view({'get': 'list'})),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]