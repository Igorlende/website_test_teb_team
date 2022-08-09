from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import AuthForm, UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import UserId
from .api_keitaro import get_clicks_and_conversations
import re

# Create your views here.


def get_clicks_and_conversations_by_custom_date(request):
    if request.method == "GET":
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        if to_date == "":
            to_date = None
        if from_date == "":
            from_date = None
        if from_date is not None or to_date is not None:
            if from_date is not None:
                if re.search("^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$", from_date) is None:
                    return HttpResponse('data not valid', status=400)
            if to_date is not None:
                if re.search("^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$", to_date) is None:
                    return HttpResponse('data not valid', status=400)
            range_for_request = {
                "from": from_date,
                "to": to_date,
                "timezone": "UTC",
                "interval": None
            }
            resp = get_clicks_and_conversations(range_for_request)
            if resp is False:
                return HttpResponse('some problem with requests in server', status=400)
            clicks = resp[0]['total']
            conversations = resp[1]['total']
            data = {"clicks": clicks, "conversations": conversations}
            return HttpResponse(json.dumps(data), status=200)
        else:
            return HttpResponse('in method must be parameters from or to', status=400)
    else:
        return HttpResponse('method must be get', status=400)


def home(request):
    if request.method == "GET":
        interval = request.GET.get('interval')
        if interval is None:
            range_for_request = {
                "from": None,
                "to": None,
                "timezone": "UTC",
                "interval": "today"
            }
            resp = get_clicks_and_conversations(range_for_request)
            if resp is False:
                return HttpResponse('some problem with requests in server', status=400)
            clicks = resp[0]['total']
            conversations = resp[1]['total']
            context = {"clicks": clicks, "conversations": conversations}
            return render(request, 'home.html', context=context)
        else:
            range_for_request = {
                "from": None,
                "to": None,
                "timezone": "UTC",
                "interval": interval
            }
            resp = get_clicks_and_conversations(range_for_request)
            if resp is False:
                return HttpResponse('some problem with requests in server', status=400)
            clicks = resp[0]['total']
            conversations = resp[1]['total']
            context = {"clicks": clicks, "conversations": conversations}
            return render(request, 'home.html', context=context)
    else:
        return HttpResponse('method must be get', status=400)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")


def login_request(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthForm()
    return render(request=request, template_name="registration/login.html",
                  context={"form": form}, )


@csrf_exempt
def register_user_request(request):
    if request.method == "POST":
        body = json.loads(request.body)
        form_data = body
        f = UserRegisterForm(form_data)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user_id = f.cleaned_data['user_id']
            try:
                if User.objects.get(username=username) is not None:
                    return HttpResponse('username exist', status=400)
            except User.DoesNotExist:
                pass
            user = User.objects.create_user(username=username,
                                            password=password)
            UserId.objects.create(userid=user_id, user=user)
            return HttpResponse('success', status=200)
        else:
            return HttpResponse('data not valid', status=400)
    else:
        return HttpResponse('method must be post', status=400)



