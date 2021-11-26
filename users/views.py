
from django.contrib.auth.models import Group
from django.views import generic
from django.urls import reverse_lazy

from warehouse.permissions_mixin import CanCreateWorkers
from .models import User
from .forms import AdminUserForm, WorkerUserForm


class AdminUserSignUpView(generic.CreateView):
    model = User
    form_class = AdminUserForm
    template_name = "users/signup.html"

    def get_success_url(self):
        return reverse_lazy("login")


class WorkerUserListView(CanCreateWorkers, generic.ListView):
    template_name = "users/list-user.html"

    def get_queryset(self):
        return Group.objects.get(name="workers").user_set.all()


class WorkerUserCreationView(CanCreateWorkers, generic.CreateView):
    model = User
    form_class = WorkerUserForm
    template_name = "users/create-worker.html"

    def get_success_url(self):
        return reverse_lazy("worker-list")
