"""
URL configuration for staffmanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from management import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("index/", views.index),
    
    # Department Management
    path("department/list/", views.department_list),
    path("department/create/", views.department_create),
    path("department/delete/", views.department_delete),
    # <int:nid> means that the URL must include a integer number in the specified position as listed below: 
    # http://127.0.0.1:8000/department/2/edit/
    # http://127.0.0.1:8000/department/3/edit/
    # http://127.0.0.1:8000/department/10/edit/
    path("department/<int:nid>/edit/", views.department_edit),
    # ----------------------------------------------------------------------------------------------------
    # Staff Management
    path("staff/list/", views.staff_list),
    # path("staff/create/", views.staff_create),
    # Create New Staff via ModelForm
    path("staff/create/modelform/", views.staff_create_modelform),
    path("staff/<int:id>/edit/", views.staff_edit),
    path("staff/<int:id>/delete/", views.staff_delete),
    # -----------------------------------------------------------------------------------------------------
    # Task Management
    path("task/list/", views.task_list),
    path("task/create/", views.task_create),
    path("task/<int:id>/edit/", views.task_edit),
    path("task/<int:id>/delete/", views.task_delete),
    # -----------------------------------------------------------------------------------------------------
    # Admin Management
    path("admin/list/", views.admin_list),
    path("admin/create/", views.admin_create),
    path("admin/<int:id>/edit/", views.admin_edit),
    path("admin/<int:id>/delete/", views.admin_delete),
    # -----------------------------------------------------------------------------------------------------
    # Login Management
    path("login/", views.login),
    # Logout Management
    path("logout/", views.logout),
    # Random image
    path("image/random/", views.image_random),
    # -----------------------------------------------------------------------------------------------------
    # Order Management
    path("order/list/", views.order_list),
    path("order/create/", views.order_create),
    path("order/delete/", views.order_delete),
    path("order/info/", views.order_info),
    path("order/edit/", views.order_edit),
   
    
    
    
]   