from django.urls import path
from .views import TaskManagement
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('tasks/', csrf_exempt(TaskManagement.as_view()), name='task-list-create'),
    path('tasks/<int:id>/', csrf_exempt(TaskManagement.as_view()), name='task-detail-update-delete'),
    path('tasks/status_filtered_list/', csrf_exempt(TaskManagement.as_view()), name='task-list-with-status-filter'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]