# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Syslog(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.CharField(
        'Device id', max_length=255, blank=True, null=True)
    facility = models.CharField(max_length=255, blank=True, null=True)
    priority = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(
        'Date', max_length=255, blank=True, null=True)
    program = models.CharField(
        'Programa', max_length=255, blank=True, null=True)
    msg = models.CharField('Message', max_length=600, blank=True, null=True)
    seq = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'syslog'
        verbose_name = 'WIFI Syslog'
        verbose_name_plural = 'WIFI Syslog'
        indexes = [
            models.Index(fields=['device_id'], name='device_id_idx'),
            models.Index(fields=['timestamp'], name='timestamp_idx'),
            models.Index(fields=['program'], name='program_idx'),
            models.Index(fields=['msg'], name='msg_idx'),
        ]


class ApnSyslog(models.Model):
    timestamp = models.DateTimeField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    domain = models.CharField(max_length=600, blank=True, null=True)
    client = models.CharField(max_length=255, blank=True, null=True)
    forward = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'queries'
        verbose_name = 'APN Syslog'
        verbose_name_plural = 'APN Syslog'
        indexes = [
            models.Index(fields=['timestamp'], name='timestamp_apn_idx'),
            models.Index(fields=['domain'], name='domain_idx'),
            models.Index(fields=['client'], name='client_idx'),
        ]
