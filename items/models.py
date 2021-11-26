
from django.db import models
from django.urls import reverse

from users.models import User


class Item(models.Model):
    stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=200)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse("edit-item", kwargs={"pk": self.id})

    def get_add_stock_url(self):
        return reverse("add-stock", kwargs={"pk": self.id})

    def get_ship_stock_url(self):
        return reverse("ship-stock", kwargs={"pk": self.id})


class ItemStockAudit(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, editable=False)
    from_value = models.PositiveIntegerField(editable=False)
    to_value = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, editable=False, null=True)

    def __str__(self):
        return self.created_at.__str__()


class TransactionAudit(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, editable=False, null=True)
    from_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    to_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, editable=False, null=True)

    def __str__(self):
        return self.created_at.__str__()

