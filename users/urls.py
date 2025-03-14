from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users_auth.views import google_login_callback, validate_google_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
    path('callback/', google_login_callback, name='callback'),
    path('auth/google/validate_token/', validate_google_token, name='validate_token'),

    # path('auth/social/', include('allauth.socialaccount.urls')),  # Social account URLs
    # path('auth/google/', include('allauth.socialaccount.providers.google.urls')), 
]
