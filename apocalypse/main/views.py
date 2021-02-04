from django.shortcuts import render, redirect
from . import models
from .models import auth_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
import mimetypes
from django.http import HttpResponse


def index(request):
    return render(request, 'main/main.html')


def statistics(request):
    cd_stats_list, cw_stats_list, cm_stats_list, pd_stats_list, pw_stats_list, pm_stats_list = models.statistics.find_players(self=1)

    ladders = {
        'daily': cd_stats_list,
        'weekly': cw_stats_list,
        'monthly': cm_stats_list
    }
    pastladders = {
        'daily': pd_stats_list,
        'weekly': pw_stats_list,
        'monthly': pm_stats_list
    }

    return render(request, 'main/statistics.html', {'currentladders': ladders, 'pastladders': pastladders})


def login(request):
    form = auth_form
    if request.method == 'POST':
        req = request.POST
        username = req.get('username')
        password = req.get('password')

        auth_check = models.authCheck.auth_check(login=username, password=password, self=1)
        if auth_check:
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('/')

    context = {'form': form}

    return render(request, 'main/index.html', context)


def signIn(request):
    if request.method == 'POST':
        req = request.POST
        username = req.get('username')
        password = req.get('password')
        nickname = req.get('nickname')

        registration = models.registration.reg(self=1, login=username, password=password, nickname=nickname)

        if registration:
            user = User.objects.create_user(username, '', password)
            user.save()
            return redirect('/')

    context = {'form': auth_form}
    return render(request, 'main/sign.html', context)


def myprofile(request):
    nick, total_points, games_played, max_points, max_daily_points, max_weekly_points, max_monthly_points = models.MyStats.check_stats(self=1, login=request.user.username)
    place_in_daily, place_in_weekly, place_in_monthly = models.MyStats.places(self=1, login=request.user.username)

    mystats = {
        'Total points': total_points,
        'Games played': games_played,
        'Max points': max_points,
        'Max daily points': max_daily_points,
        'Max weekly points': max_weekly_points,
        'Max monthly points': max_monthly_points,

    }

    myplaces = {

        'Daily': place_in_daily,
        'Weekly': place_in_weekly,
        'Monthly': place_in_monthly,

    }

    return render(request, 'main/myprofile.html', {'mystats': mystats, 'myplaces': myplaces, 'nick': nick})


def log_out(request):
    logout(request)
    return redirect('/')
