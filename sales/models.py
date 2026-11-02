from django.conf import settings
from django.db import models

class Company(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='octax_companies')
    name = models.CharField('Название компании', max_length=180)
    industry = models.CharField('Отрасль', max_length=120, blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=40, blank=True)
    website = models.URLField('Сайт', blank=True)
    city = models.CharField('Город', max_length=120, blank=True)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
    def __str__(self): return self.name

class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        CONTACTED = 'contacted', 'Связались'
        QUALIFIED = 'qualified', 'Квалифицирован'
        LOST = 'lost', 'Не заинтересован'
        CONVERTED = 'converted', 'Преобразован в клиента'
    class Source(models.TextChoices):
        WEBSITE = 'website', 'Сайт'
        REFERRAL = 'referral', 'Рекомендация'
        SOCIAL = 'social', 'Соцсети'
        OTHER = 'other', 'Другое'
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='octax_leads')
    name = models.CharField('Имя', max_length=180)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=40, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW)
    source = models.CharField('Источник', max_length=20, choices=Source.choices, default=Source.OTHER)
    notes = models.TextField('Заметки', blank=True)
    converted_client = models.OneToOneField('crm.Client', on_delete=models.SET_NULL, null=True, blank=True, related_name='source_lead')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
    def __str__(self): return self.name
