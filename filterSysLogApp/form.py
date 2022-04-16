from django.forms import ModelForm
from .models import Syslog


class SyslogForm(ModelForm):
    class Meta:
        model = Syslog
        fields = ['program', 'device_id', 'timestamp', 'timestamp']
