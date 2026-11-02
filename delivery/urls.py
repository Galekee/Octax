from django.urls import path
from .views import dashboard
urlpatterns=[path("",dashboard,name="delivery_dashboard")]
