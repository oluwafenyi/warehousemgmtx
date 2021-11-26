
from django import forms
from django.core.exceptions import ValidationError

from warehouse.utils import LockedAtomicTransaction
from .models import Item, ItemStockAudit, TransactionAudit


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "selling_price"]


class StockIncreaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            self.item: Item = kwargs.pop("item")
        except KeyError:
            self.item = None
        try:
            self.request = kwargs.pop("request")
        except KeyError:
            self.request = None
        super().__init__(*args, **kwargs)

    quantity = forms.IntegerField(min_value=1, label="Quantity to Add to Stock")

    def save(self):
        with LockedAtomicTransaction(Item):
            self.item.refresh_from_db()
            item = self.item
            current_stock = item.stock
            new_value = self.cleaned_data["quantity"] + current_stock
            item.stock = new_value
            item.save()
            ItemStockAudit.objects.create(
                item=item,
                from_value=current_stock,
                to_value=new_value,
                created_by=self.request.user
            )
        return item


class StockDecreaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            self.item = kwargs.pop("item")
        except KeyError:
            self.item = None
        try:
            self.request = kwargs.pop("request")
        except KeyError:
            self.request = None
        super().__init__(*args, **kwargs)

    quantity = forms.IntegerField(min_value=1, label="Quantity to Ship")

    def save(self):
        quantity = self.cleaned_data["quantity"]
        with LockedAtomicTransaction(Item):
            self.item.refresh_from_db()
            item = self.item
            current_stock = item.stock
            if quantity > current_stock:
                raise ValidationError("You can't ship more than your current stock")
            new_value = current_stock - quantity
            item.stock = new_value
            item.save()
            ItemStockAudit.objects.create(
                item=item,
                from_value=current_stock,
                to_value=new_value,
                created_by=self.request.user
            )

            try:
                last_record = TransactionAudit.objects.filter(item=item).latest("created_at")
                from_value = last_record.to_value
            except TransactionAudit.DoesNotExist:
                from_value = 0

            TransactionAudit.objects.create(
                item=item,
                from_value=from_value,
                to_value=from_value + (quantity * item.selling_price),
                created_by=self.request.user
            )
        return item
