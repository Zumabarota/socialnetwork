from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views

app_name = "dwitter"

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'dweet', views.DweetViewSet, basename='dweet')
router.register(r'comment', views.CommentViewSet, basename='comment')

urlpatterns = format_suffix_patterns([
    path("accounts/", include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
])
urlpatterns += router.urls
