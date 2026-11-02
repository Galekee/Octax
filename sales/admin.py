from django.contrib import admin
from .models import Lead, Company
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name','status','source','owner','created_at')
    list_filter = ('status','source')
    search_fields = ('name','email','phone')
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','industry','owner','created_at')
    search_fields = ('name','email','phone')
