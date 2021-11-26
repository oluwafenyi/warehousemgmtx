from datetime import timedelta, datetime


from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic

from warehouse.permissions_mixin import CanViewStats
from items.models import ItemStockAudit, TransactionAudit
from .forms import ReportForm


class ReportView(CanViewStats, generic.View):
    def get(self, request):
        start_date = (timezone.now() - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0).date()
        end_date = timezone.now().date()
        form = ReportForm(data={"start_date": start_date, "end_date": end_date})
        stock_audit = []
        transaction_audit = []
        return render(request, "reports/index.html", {"form": form, "stock_audit": stock_audit, "transaction_audit": transaction_audit})

    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            item = form.data["item"]
            start_date = datetime.strptime(form.data["start_date"], "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            start_date = timezone.make_aware(start_date)
            end_date = datetime.strptime(form.data["end_date"], "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=0)
            end_date = timezone.make_aware(end_date)
            stock_audit = ItemStockAudit.objects.filter(created_at__gte=start_date, created_at__lte=end_date, item_id=item).order_by("created_at").all()
            transaction_audit = TransactionAudit.objects.filter(created_at__gte=start_date, created_at__lte=end_date, item_id=item).order_by("created_at").all()
            return render(request, "reports/index.html", {"form": form, "stock_audit": stock_audit, "transaction_audit": transaction_audit})
        return redirect("reports")
