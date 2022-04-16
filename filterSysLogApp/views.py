from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from .models import Syslog
from datetime import datetime, date

# Create your views here.


def noAutenticate(request):
    return render(request, 'pagesError401.html')


@login_required(login_url='/login/')
def profile(request):
    user = None
    # programs = Syslog.objects.all().order_by('id')

    try:
        user = User.objects.get(id=request.user.id)
    except:
        pass
    try:
        if not user.is_staff:
            return redirect("/noAutenticate/")
    except:
        pass
    # programs = Syslog.objects.order_by('program').values_list('program', 'id').distinct('program').exclude(program__icontains='%').exclude(program__icontains='/')
    # programs = Syslog.objects.filter(timestamp__icontains='28/1/2020').order_by('id')
    # programs = paginate(request, programs)
    programs = None
    context = None
    errors = []
    if request.method == 'GET':
        if not request.GET.get('programs', '') or not request.GET.get('device', '') or not request.GET.get('initDate', '') or not request.GET.get('endDate', ''):
            errors.append(
                'Por favor llene todos los campos, son requeridos.')
        else:
            programsId = int(request.GET.get('programs', ''))
            device_id = int(request.GET.get('device', ''))
            initDate = request.GET.get('initDate', '')
            endDate = request.GET.get('endDate', '')

            # initDate1 = datetime.strptime(
            #     request.GET.get('initDate', ''), '%Y-%m-%d')
            # esto es para windows quitar el cero del mes
            # initDate = datetime.strftime(initDate1, '%d/%#m/%Y')
            # initDate = datetime.strftime(initDate1, '%d/%-m/%Y') para linux quitar el cero del mes
            # endDate1 = datetime.strptime(
            #     request.GET.get('endDate', ''), '%Y-%m-%d')
            # endDate = datetime.strftime(endDate1, '%d/%#m/%Y')

            if programsId:
                if programsId == 5:
                    programs = Syslog.objects.filter(
                        program__contains='DHCPD').order_by('id')
            if device_id >= 1:
                id = str(device_id)
                programsDiviceId = programs.filter(
                    device_id__icontains=id).order_by('id')
                if programsDiviceId:
                    programs = programsDiviceId
            if initDate:
                fecha = str(initDate)
                programsDate = programs.filter(
                    timestamp__icontains=fecha).order_by('id')
                if programsDate:
                    programs = programsDate

            paginator = Paginator(programs, 1000)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            # programs = paginate(request, programs)
            # try:
            #     page_obj = paginator.page(page)
            # except PageNotAnInteger:
            #     # If page is not an integer, deliver first page.
            #     page_obj = paginator.page(1)
            # except EmptyPage:
            #     # If page is out of range (e.g. 9999), deliver last page of results.
            #     page_obj = paginator.page(paginator.num_pages)
            parametros = request.GET.copy()
            if parametros.__contains__('page'):
                del parametros['page']

            context = {
                "user": user,
                "programs": programs,
                "parametros": parametros,
            }
            return render(request, 'profile.html', {"user": user, "programs": programs, "parametros": parametros, 'page_obj': page_obj, })

    return render(request, 'profile.html', {'errors': errors})


def paginate(request, obj):
    """"Paginado"""
    page = request.GET.get('page')
    paginator = Paginator(obj, 1000)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
