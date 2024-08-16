from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import EmailVerifyRecord, UserProfile
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
# Create your views here.


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def active_user(request, active_code):
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('link error')
    return redirect('users:login')


def login_view(request):

    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username: {username}, Password: {password}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:user_profile')
            else:
                return HttpResponse('login failed!')

    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            new_user.save()

            # send email
            send_register_email(form.cleaned_data.get('email'),'register')

            return HttpResponse("Registration succeed!")

    context = {'form': form}
    return render(request, 'users/register.html', context)


# 检测登录的装饰器
@login_required(login_url='users:login')
def user_profile(request):
    user = User.objects.get(username=request.user)
    return render(request, 'users/user_profile.html', {'user': user})


def forget_pwd(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            exists = User.objects.filter(email=email).exists()
            if exists:
                send_register_email(email, 'forget')
                return HttpResponse('Email sent!')
            else:
                return HttpResponse('Typed email is not registered!')
    return render(request, 'users/forget_pwd.html', {'form': form})

def forget_pwd_url(request, active_code):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('Modification succeed!')
        else:
            return HttpResponse('Modification failed!')

    return render(request, 'users/reset_pwd.html', {'form': form})
