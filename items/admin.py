
from django.contrib import admin

from .models import Item, ItemStockAudit, TransactionAudit


admin.site.register(Item)
admin.site.register(ItemStockAudit)
admin.site.register(TransactionAudit)
