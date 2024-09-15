from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # URL for user registration
    path('auth/register/', csrf_exempt(views.UserAuth.as_view()), name='user-registration'),
    path('auth/', csrf_exempt(views.UserAuth.as_view()), name='user-login'),
]