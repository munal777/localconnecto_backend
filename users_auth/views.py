from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from rest_framework import status



User = get_user_model()


@login_required
def google_login_callback(request):
    user = request.user

    social_accounts = SocialAccount.objects.filter(user=user)
    print("social account for user:", social_accounts)

    social_account = social_accounts.first()

    if not social_account:
        print("No social account for user:", user)
        return redirect('http://localhost:5173/login/callback/?error=NoSocialAccount')
    
    token = SocialToken.objects.filter(account=social_account, account__provider='google').first()

    if token:
        print('Google token found:', token.token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return redirect(f'http://localhost:5173/login/callback/?access_token={access_token}')

    else:
        print('No Google token found for user', user)
        return redirect(f'http://localhost:5173/login/callback/?error=NoGoogleToken')
    


@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            google_access_token = data.get('access_token')
            print(google_access_token)

            if not google_access_token:
                return JsonResponse({'details': 'Access Token is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({'valid': True}, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return JsonResponse({'details': 'Invalid JSON.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({'details': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            



        