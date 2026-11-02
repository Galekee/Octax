from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('crm', '0003_clientportalprofile_portalrequest_and_more')]
    operations = [
        migrations.AddField(
            model_name='registrationrequest',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]
