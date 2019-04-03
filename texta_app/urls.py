from django.urls import path
from texta_api.views import dataset_controller, upload_dataset, dataset_controller_delete_row

urlpatterns = [
    path('dataset/', dataset_controller),
    path('dataset/<int:id>/', dataset_controller),
    path('dataset/<int:id>/datarow/<int:row_id>', dataset_controller_delete_row),
    path('dataset/<int:id>/upload', upload_dataset),
]
