
from django.shortcuts import render
from django.views import generic

from items.models import Item, TransactionAudit


class IndexView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            total_revenue = None
            if request.user.has_perm("items.can_view_stats"):
                total = 0
                query = TransactionAudit.objects.raw("SELECT max(audit.id) as id from items_transactionaudit as audit group by audit.item_id")
                for r in query:
                    total += r.to_value
                total_revenue = total
            context = {"object_list": Item.objects.all().order_by("id"), "total_revenue": total_revenue}
            return render(request, "items/item-list.html", context=context)
        return render(request, "warehouse/index.html")
