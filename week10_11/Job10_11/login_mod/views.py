from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .form import LoginForm


def index(request):
    return HttpResponse("Hello Django!")


def login_action(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # 登陆用户
                login(request, user)
                return redirect('/hello')
            else:
                return HttpResponse('登录失败')
    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form.html', {'form': login_form})
