"""texta_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from texta_api.views import dataset_controller, upload_dataset, datarows_view, dataset_controller_delete_row

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dataset/', dataset_controller),
    path('dataset/<int:id>/', dataset_controller),
    path('dataset/<int:id>/datarow/<int:row_id>', dataset_controller_delete_row),
    path('dataset/<int:id>/upload', upload_dataset),
    path('datarows/', datarows_view)
]
