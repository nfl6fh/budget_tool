from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_transaction/", views.add_transaction, name="add_transaction"),
    path("add_category/", views.add_category, name="add_category"),
    path("settings/", views.settings_page, name="settings_page"),
    path("add_source/", views.add_source, name="add_source"),
    path("edit_source/<int:source_id>/", views.edit_source, name="edit_source"),  # Placeholder for editing a source
    path("edit_category/<int:category_id>/", views.edit_category, name="edit_category"),  # Placeholder for editing a category
    path("edit_transaction/<int:transaction_id>/", views.edit_transaction, name="edit_transaction"),  # Placeholder for editing a transaction
    path("delete_source/<int:source_id>/", views.delete_source, name="delete_source"),
    path("delete_category/<int:category_id>/", views.delete_category, name="delete_category"),
    path("delete_transaction/<int:transaction_id>/", views.delete_transaction, name="delete_transaction"),
]