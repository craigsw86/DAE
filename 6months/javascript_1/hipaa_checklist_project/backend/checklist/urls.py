from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegulationUpdateViewSet, ChecklistItemViewSet

router = DefaultRouter()
router.register(r'regulations', RegulationUpdateViewSet)
router.register(r'checklist', ChecklistItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
