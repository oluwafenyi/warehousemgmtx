
from django.contrib.auth.models import Group
from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        abstract = True
        fields = ["firstname", "lastname", "email", "password", "confirm_password"]
        labels = {
            "firstname": "First Name",
            "lastname": "Last Name",
            "password": "Password",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "Your passwords do not match"
            )
        return cleaned_data


class AdminUserForm(UserForm):
    def save(self, commit=True):
        data = {**self.cleaned_data}
        data.pop("confirm_password")
        password = data.pop("password")
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        admins = Group.objects.get(name="administrators")
        user.groups.add(admins)
        return user


class WorkerUserForm(UserForm):
    def save(self, commit=True):
        data = {**self.cleaned_data}
        data.pop("confirm_password")
        password = data.pop("password")
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        user.groups.add(Group.objects.get(name="workers"))
        return user
