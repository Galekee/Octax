from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='finance_dashboard'),
    path('sla/', views.sla_dashboard, name='finance_sla'),
    path('export/', views.export_csv, name='finance_export'),
    path('documents/<slug:slug>/', views.document_download, name='finance_document'),
    path('new/', views.entry_form, name='finance_new'),
    path('<int:pk>/edit/', views.entry_form, name='finance_edit'),
    path('<int:pk>/delete/', views.entry_delete, name='finance_delete'),
]
