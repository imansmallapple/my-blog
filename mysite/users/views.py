from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.


def login_view(request):

    if request.method == 'POST':
        ##  获取表单中的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        ##  与数据库中的用户名和密码比对
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Login succeed!')
        else:
            return HttpResponse('Login failed!')
    return render(request, 'users/login.html')