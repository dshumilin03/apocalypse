from django.db import models
import cgi
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class querry(models.Manager):

    def q(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""SELECT user_nickname, max_monthly_points FROM statistics ORDER BY max_monthly_points DESC 
            LIMIT 5""")
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row)
        return result_list


class authCheck(models.Manager):
    def auth_check(self, login, password):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT login, user_password FROM players where login = '{}' and user_password = '{}'".format
                           (login, password))
            result_list = cursor.fetchone()
            if result_list != None:
                if result_list[1] == password:
                    return True


class registration(models.Manager):
    def reg(self, login, nickname, password):
        from django.db import connection, IntegrityError
        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO players(nickname, login, user_password) VALUES('{}', '{}', '{}')".format(
                    nickname, login, password))
            except IntegrityError:
                return False
            queries = [
                   "INSERT INTO daily_current_ladder(user_nickname, user_max_daily_points) VALUES('{}', 0)",
                   "INSERT INTO weekly_current_ladder(user_nickname, user_max_weekly_points) VALUES('{}', 0)",
                   "INSERT INTO monthly_current_ladder(user_nickname, user_max_monthly_points) VALUES('{}', 0)",
                   "INSERT INTO daily_past_ladder(user_nickname, user_past_daily_points) VALUES('{}', 0)",
                   "INSERT INTO weekly_past_ladder(user_nickname, user_past_weekly_points) VALUES('{}', 0)",
                   "INSERT INTO monthly_past_ladder(user_nickname, user_past_monthly_points) VALUES('{}', 0)",
                   "INSERT INTO inventory(user_nickname, space_ship2, space_ship3) VALUES('{}', false, false)",
                   "INSERT INTO statistics(user_nickname, max_points, total_points, games_played, max_daily_points, "
                   "max_weekly_points, max_monthly_points) VALUES('{}', 0, 0, 0, 0, 0, 0)"]
            for elem in queries:
                cursor.execute(elem.format(nickname))
        return True


class user_settings(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.username, self.password




class auth_form(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': '',
        'type': '',
        'placeholder': 'username',

    }), label='')
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': '',
        'type': 'password',
        'placeholder': 'password',

    }), label='')

    nickname = forms.CharField(widget=forms.TextInput(attrs={
        'class': '',
        'type': '',
        'placeholder': 'nickname',

    }), label='')

    repp = forms.CharField(widget=forms.TextInput(attrs={
        'class': '',
        'type': 'password',
        'placeholder': 'repeat password',

    }), label='')

    class Meta:
        model = user_settings
        fields = '__all__'


class statistics(models.Manager):
    def find_players(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_nickname FROM daily_current_ladder ORDER BY user_max_daily_points DESC LIMIT 5")
            cd_stats_list = cursor.fetchall()
            cursor.execute("SELECT user_nickname FROM weekly_current_ladder ORDER BY user_max_weekly_points DESC LIMIT 5")
            cw_stats_list = cursor.fetchall()
            cursor.execute("SELECT user_nickname FROM monthly_current_ladder ORDER BY user_max_monthly_points DESC LIMIT 5")
            cm_stats_list = cursor.fetchall()

            cursor.execute("SELECT user_nickname FROM daily_past_ladder ORDER BY user_past_daily_points DESC LIMIT 5")
            pd_stats_list = cursor.fetchall()
            cursor.execute("SELECT user_nickname FROM weekly_past_ladder ORDER BY user_past_weekly_points DESC LIMIT 5")
            pw_stats_list = cursor.fetchall()
            cursor.execute("SELECT user_nickname FROM monthly_past_ladder ORDER BY user_past_monthly_points DESC LIMIT 5")
            pm_stats_list = cursor.fetchall()
        cd_stats_list1 = []
        cw_stats_list1 = []
        cm_stats_list1 = []
        pd_stats_list1 = []
        pw_stats_list1 = []
        pm_stats_list1 = []

        for elem in cd_stats_list:
            for el in elem:
                cd_stats_list1.append(el)

        for elem in cw_stats_list:
            for el in elem:
                cw_stats_list1.append(el)

        for elem in cm_stats_list:
            for el in elem:
                cm_stats_list1.append(el)

        for elem in pd_stats_list:
            for el in elem:
                pd_stats_list1.append(el)

        for elem in pw_stats_list:
            for el in elem:
                pw_stats_list1.append(el)

        for elem in pm_stats_list:
            for el in elem:
                pm_stats_list1.append(el)
        return cd_stats_list1, cw_stats_list1, cm_stats_list1, pd_stats_list1, pw_stats_list1, pm_stats_list1


class MyStats(models.Manager):

    def check_stats(self, login):
        from django.db import connection
        with connection.cursor() as cursor:
            query1 = "select nickname from players where login = '{}' ".format(login)
            cursor.execute(query1)
            nick = cursor.fetchone()[0]
            query2 = "select * from statistics where user_nickname = '{}'".format(nick)
            cursor.execute(query2)
            data = cursor.fetchall()
            nick = data[0][0]
            max_points = data[0][1]
            total_points = data[0][2]
            games_played = data[0][3]
            max_daily_points = data[0][4]
            max_weekly_points = data[0][5]
            max_monthly_points = data[0][6]
        return nick, total_points, games_played, max_points, max_daily_points, max_weekly_points, max_monthly_points


    def places(self, login):

        from django.db import connection
        with connection.cursor() as cursor:
            query1 = "select nickname from players where login = '{}' ".format(login)
            cursor.execute(query1)
            nick = cursor.fetchone()[0]

            query = 'select * from daily_current_ladder order by user_max_daily_points desc'
            cursor.execute(query)
            daily_table = cursor.fetchall()
            place_in_daily = 1
            detect = False
            for elem in daily_table:
                if not detect:

                    for sec_elem in elem:
                        if nick in str(sec_elem):
                            detect = True
                            break
                    if not detect:
                        place_in_daily += 1
            # daily place ready

            query = 'select * from weekly_current_ladder order by user_max_weekly_points desc'
            cursor.execute(query)
            weekly_table = cursor.fetchall()
            place_in_weekly = 1
            detect = False
            for elem in weekly_table:
                if not detect:
                    for sec_elem in elem:
                        if nick in str(sec_elem):
                            detect = True
                            break
                    if not detect:
                        place_in_weekly += 1
            # weekly place ready

            query = 'select * from monthly_current_ladder order by user_max_monthly_points desc'
            cursor.execute(query)
            monthly_table = cursor.fetchall()
            place_in_monthly = 1
            detect = False
            for elem in monthly_table:
                if not detect:
                    for sec_elem in elem:
                        if nick in str(sec_elem):
                            detect = True
                            break
                    if not detect:
                        place_in_monthly += 1
            # monthly place ready
            return place_in_daily, place_in_weekly, place_in_monthly
