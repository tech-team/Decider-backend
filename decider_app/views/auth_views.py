# coding=utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json
from decider_app.models import User


@require_http_methods(['GET'])
def login_view(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'login.html', c)


@require_http_methods(['GET'])
def registration_view(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'registration.html', c)


@require_http_methods(['POST'])
def submit_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email and password:
        user = authenticate(email=email, password=password)
        if not user:
            return HttpResponse(json.dumps({"status": "ERROR", "error": u"Неправильные данные"}), content_type="application/json")
        else:
            login(request, user)
            return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "ERROR", "error": u"Мало данных"}), content_type="application/json")


@require_http_methods(['POST'])
def submit_registration(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if username and email and password:
        try:
            user = User.objects.get(email=email)
            if user:
                return HttpResponse(json.dumps({"status": "ERROR", "error": u"email занят"}), content_type="application/json")
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=username)
            user.set_password(request.POST["password"])
            user.save()

            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "ERROR", "error": u"Ошибочка вышла"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "ERROR", "error": u"Мало данных"}, content_type="application/json"))


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')
