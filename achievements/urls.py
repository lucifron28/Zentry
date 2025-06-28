from django.urls import path
from . import views

urlpatterns = [
    path('badges/', views.BadgeListView.as_view(), name='badge-list'),
    path('user-badges/', views.UserBadgeListView.as_view(), name='user-badges'),
    path('check-badges/', views.check_badge_eligibility, name='check-badges'),
]
