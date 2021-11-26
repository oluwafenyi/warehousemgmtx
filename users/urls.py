
from django.urls import path

from .views import AdminUserSignUpView, WorkerUserCreationView, WorkerUserListView


urlpatterns = [
    path("signup/", AdminUserSignUpView.as_view(), name="admin-user-signup"),
    path("worker/", WorkerUserListView.as_view(), name="worker-list"),
    path("worker/add/", WorkerUserCreationView.as_view(), name="worker-creation"),
]
