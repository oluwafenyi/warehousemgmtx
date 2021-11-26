
from django.urls import path

from .views import ItemCreationView, ItemEditView, ItemStockAddView, ItemStockDecreaseView


urlpatterns = [
    path("create/", ItemCreationView.as_view(), name="create-item"),
    path("<int:pk>/edit/", ItemEditView.as_view(), name="edit-item"),
    path("<int:pk>/add/", ItemStockAddView.as_view(), name="add-stock"),
    path("<int:pk>/ship/", ItemStockDecreaseView.as_view(), name="ship-stock"),
]
