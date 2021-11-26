from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase

from users.models import User
from .utils import setup_user


class UserViewTests(TestCase):
    def test_admin_user_creation(self):
        url = reverse("admin-user-signup")
        data = {
            "firstname": "Admin",
            "lastname": "User",
            "email": "admin@warehouse.com",
            "password": "WorkerAdmin2021",
            "confirm_password": "WorkerAdmin2021"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())
        self.assertTrue(User.objects.get(email=data["email"]).groups.filter(name="administrators").exists())

    def test_admin_user_create_worker(self):
        admin = setup_user("admin@warehouse.com", "administrators")
        self.client.login(username=admin.email, password="WorkerAdmin2021")
        data = {
            "firstname": "Worker",
            "lastname": "User",
            "email": "worker@warehouse.com",
            "password": "WorkerAdmin2021",
            "confirm_password": "WorkerAdmin2021"
        }
        url = reverse("worker-creation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_list_workers_by_admin(self):
        admin = setup_user("admin@warehouse.com", "administrators")
        self.client.login(username=admin.email, password="WorkerAdmin2021")
        url = reverse("worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_workers_by_worker(self):
        worker = setup_user("worker@warehouse.com", "workers")
        self.client.login(username=worker.email, password="WorkerAdmin2021")
        url = reverse("worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)