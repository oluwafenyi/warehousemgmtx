
from django.contrib.auth.models import Group

from users.models import User


def setup_user(email, group):
    user = User.objects.create(firstname="Admin", lastname="User", email=email)
    Group.objects.get(name=group).user_set.add(user)
    user.set_password("WorkerAdmin2021")
    user.save()
    return user
