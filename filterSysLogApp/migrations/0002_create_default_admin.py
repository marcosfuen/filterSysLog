from decouple import config
from django.db import migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('filterSysLogApp', '0001_initial'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DEFAULT_SUPERUSER_NAME = config(
            'DEFAULT_SUPERUSER_NAME', default='admin')
        DEFAULT_SUPERUSER_EMAIL = config(
            'DEFAULT_SUPERUSER_EMAIL', default='admin@example.com')
        DEFAULT_SUPERUSER_PASSWORD = config(
            'DEFAULT_SUPERUSER_PASSWORD', default='secret')

        superuser = User.objects.create_superuser(
            username=DEFAULT_SUPERUSER_NAME,
            email=DEFAULT_SUPERUSER_EMAIL,
            password=DEFAULT_SUPERUSER_PASSWORD,
            last_login=datetime.date.today())
        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
