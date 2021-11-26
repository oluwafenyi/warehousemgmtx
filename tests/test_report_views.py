from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase

from .utils import setup_user


class ReportViewTests(TestCase):
    def test_worker_view_reports(self):
        worker = setup_user("worker@warehouse.com", "workers")
        self.client.login(username=worker.email, password="WorkerAdmin2021")
        url = reverse("reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_admin_view_reports(self):
        admin = setup_user("admin@warehouse.com", "administrators")
        self.client.login(username=admin.email, password="WorkerAdmin2021")
        url = reverse("reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
