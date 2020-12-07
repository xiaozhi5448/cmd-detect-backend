from django.db import models
from django.utils import timezone
# Create your models here.


class MisAlarmCommand(models.Model):
    # id = models.IntegerField(auto_created=True, db_column='id', primary_key=True)
    command = models.CharField(max_length=2000, db_column='command')
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mis_alarm_commands'

class NewBusiness(models.Model):

    ip_addr = models.CharField(max_length=16, db_column='ip_addr', unique=True)
    count = models.IntegerField(verbose_name='连续告警次数', default=0)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'new_business_ip'

