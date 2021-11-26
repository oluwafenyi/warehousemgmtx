
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from warehouse.permissions_mixin import CanAdministerItem

from .models import Item
from .forms import ItemForm, StockIncreaseForm, StockDecreaseForm


class ItemCreationView(CanAdministerItem, generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = "items/item-creation.html"

    def get_success_url(self):
        return reverse_lazy("home")


class ItemEditView(CanAdministerItem, generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "items/item-creation.html"

    def get_success_url(self):
        return reverse_lazy("home")


class ItemStockAddView(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        form = StockIncreaseForm()
        context = {
            "form": form,
            "item": item
        }
        return render(request, "items/stock-increase.html", context)

    def post(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        form = StockIncreaseForm(request.POST, item=item, request=request)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, "items/stock-increase.html", context={"form": form})


class ItemStockDecreaseView(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        form = StockIncreaseForm()
        context = {
            "form": form,
            "item": item
        }
        return render(request, "items/stock-decrease.html", context)

    def post(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        form = StockDecreaseForm(request.POST, item=item, request=request)
        if form.is_valid():
            try:
                form.save()
            except ValidationError as e:
                form.errors["non_field_errors"] = e.messages
                return render(request, "items/stock-decrease.html", context={"form": form, "item": item})
            return redirect("home")
        return render(request, "items/stock-decrease.html", context={"form": form, "item": item})
