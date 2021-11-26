from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase, TransactionTestCase

from items.models import Item, ItemStockAudit, TransactionAudit
from .utils import setup_user


class ItemViewTests(TestCase):
    def test_admin_create_item(self):
        admin = setup_user("admin@warehouse.com", "administrators")
        self.client.login(username=admin.email, password="WorkerAdmin2021")
        url = reverse("create-item")
        data = {
            "name": "Some Item",
            "description": "Some Description",
            "selling_price": 700
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(Item.objects.filter(name="Some Item").exists())

    def test_admin_cant_set_item_stock(self):
        admin = setup_user("admin@warehouse.com", "administrators")
        self.client.login(username=admin.email, password="WorkerAdmin2021")
        url = reverse("create-item")
        data = {
            "name": "Some Item",
            "description": "Some Description",
            "selling_price": 700,
            "stock": 500
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(Item.objects.filter(name="Some Item").exists())
        self.assertEqual(Item.objects.get(name="Some Item").stock, 0)
        
    def test_worker_create_item(self):
        worker = setup_user("worker@warehouse.com", "workers")
        self.client.login(username=worker.email, password="WorkerAdmin2021")
        url = reverse("create-item")
        data = {
            "name": "Some Item",
            "description": "Some Description",
            "selling_price": 700
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertFalse(Item.objects.filter(name="Some Item").exists())

    def test_add_to_item_stock(self):
        worker = setup_user("worker@warehouse.com", "workers")
        self.client.login(username=worker.email, password="WorkerAdmin2021")
        item = Item.objects.create(**{
            "name": "Some Item",
            "description": "Some Description",
            "selling_price": 700
        })
        url = reverse("add-stock", kwargs={"pk": item.id})
        data = {
            "quantity": 2
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Item.objects.get(name="Some Item").stock, 2)
        self.assertEqual(ItemStockAudit.objects.filter(item=item).count(), 1)

    def test_ship_item_from_stock(self):
        worker = setup_user("worker@warehouse.com", "workers")
        self.client.login(username=worker.email, password="WorkerAdmin2021")
        stock = 500
        item = Item.objects.create(**{
            "name": "Some Item",
            "description": "Some Description",
            "selling_price": 700,
            "stock": stock
        })
        url = reverse("ship-stock", kwargs={"pk": item.id})
        quantity = 2
        data = {
            "quantity": quantity
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Item.objects.get(name="Some Item").stock, stock - quantity)
        self.assertEqual(ItemStockAudit.objects.filter(item=item).count(), 1)
        self.assertEqual(TransactionAudit.objects.filter(item=item).count(), 1)
        self.assertEqual(TransactionAudit.objects.get(item=item).to_value, quantity * item.selling_price)


class ItemViewTestsTransactions(TransactionTestCase):
    def test_ship_more_than_stock(self):
        worker = setup_user("worker@warehouse.com", "workers")
        self.client.login(username=worker.email, password="WorkerAdmin2021")
        stock = 500
        item = Item.objects.create(**{
            "name": "Some Item",
            "description": "Some Description",
            "selling_price": 700,
            "stock": stock
        })
        url = reverse("ship-stock", kwargs={"pk": item.id})
        quantity = 501
        data = {
            "quantity": quantity
        }
        self.client.post(url, data=data)
        self.assertEqual(Item.objects.get(name="Some Item").stock, stock)
        self.assertEqual(ItemStockAudit.objects.filter(item=item).count(), 0)
        self.assertEqual(TransactionAudit.objects.filter(item=item).count(), 0)
