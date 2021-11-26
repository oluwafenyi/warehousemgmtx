
from django.contrib.auth.mixins import UserPassesTestMixin


class CanCreateWorkers(UserPassesTestMixin):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.has_perm("users.can_create_workers")


class CanAdministerItem(UserPassesTestMixin):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.has_perm("items.can_administer_item")


class CanViewStats(UserPassesTestMixin):
    login_url = "/login/"

    def test_func(self):
        return self.request.user.has_perm("items.can_view_stats")
