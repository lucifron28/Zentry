from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'badges', views.BadgeViewSet)
router.register(r'user-badges', views.UserBadgeViewSet)

urlpatterns = [
    path('achievements/', include(router.urls)),
]
