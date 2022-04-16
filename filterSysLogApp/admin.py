from django.contrib import admin
from .models import Syslog, ApnSyslog
from django.db.models import F, Q, Case, When, ExpressionWrapper, BigIntegerField
from django.utils.translation import ugettext_lazy as _
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.http import HttpResponse
import csv

# Register your models here.


class InputFilter(admin.SimpleListFilter):
    template = '_admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class DeviceIdFilter(InputFilter):
    parameter_name = 'device_id'
    title = _('Device id')

    def queryset(self, request, queryset):
        if self.value() is not None:
            device_id = self.value()

            return queryset.filter(device_id=device_id)


class ProgramFilter(InputFilter):
    parameter_name = 'program'
    title = _('Program')

    def queryset(self, request, queryset):
        if self.value() is not None:
            program = self.value()

            return queryset.filter(program=program)


class MsgFilter(InputFilter):
    parameter_name = 'msg'
    title = _('Msg')

    def queryset(self, request, queryset):
        if self.value() is not None:
            msg = self.value()

            return queryset.filter(msg__contains=msg)


class ExportWifiCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            # row = [getattr(obj, field)() if callable(
            #     getattr(obj, field)) else getattr(obj, field) for field in field_names]
            # writer.writerow(row)
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class SyslogAdmin(admin.ModelAdmin, ExportWifiCsvMixin):
    search_fields = ['device_id', 'facility', 'priority',
                     'level', 'tag', 'timestamp', 'program', 'msg', 'seq']
    list_display = ('device_id', 'timestamp', 'program', 'msg')
    list_filter = (('timestamp', DateRangeFilter),
                   DeviceIdFilter, ProgramFilter, MsgFilter,)
    actions = ['export_as_csv']


class UrlFilter(InputFilter):
    parameter_name = 'domain'
    title = _('Domain')

    def queryset(self, request, queryset):
        if self.value() is not None:
            domain = self.value()

            return queryset.filter(domain__contains=domain)


class ClientFilter(InputFilter):
    parameter_name = 'client'
    title = _('Client')

    def queryset(self, request, queryset):
        if self.value() is not None:
            client = self.value()

            return queryset.filter(client=client)


class TimestampFilter(InputFilter):
    parameter_name = 'timestamp'
    title = _('Timestamp')

    def queryset(self, request, queryset):
        if self.value() is not None:
            timestamp = self.value()

            return queryset.filter(timestamp=timestamp)


class ExportApnCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            # row = [getattr(obj, field)() if callable(
            #     getattr(obj, field)) else getattr(obj, field) for field in field_names]
            # writer.writerow(row)
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ApnSyslogAdmin(admin.ModelAdmin, ExportApnCsvMixin):
    # date_hierarchy = 'timestamp'
    search_fields = ['timestamp', 'domain', 'client']
    list_display = ('timestamp', 'type', 'status',
                    'domain', 'client', 'forward')
    list_filter = (('timestamp', DateRangeFilter), UrlFilter, ClientFilter, )
    actions = ['export_as_csv']
    # list_per_page = 1000
    # empty_value_display = '-empty-'
    # list_max_show_all = 1000


admin.site.register(ApnSyslog, ApnSyslogAdmin)
admin.site.register(Syslog, SyslogAdmin)


admin.site.site_header = 'Log filtering system - Universidad de Camagüey'
admin.site.site_title = 'Log filtering system - Universidad de Camagüey'
