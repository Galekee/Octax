from django.urls import path
from . import views
urlpatterns = [
 path('<str:kind>/', views.listing, name='sales_list'),
 path('<str:kind>/new/', views.edit, name='sales_create'),
 path('<str:kind>/<int:pk>/edit/', views.edit, name='sales_edit'),
 path('<str:kind>/<int:pk>/delete/', views.delete, name='sales_delete'),
 path('leads/<int:pk>/convert/', views.convert_lead, name='sales_convert'),
]
