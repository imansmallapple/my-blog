from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import EmailVerifyRecord, UserProfile, PendingUser
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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
    for record in all_records:
        email = record.email

        try:
            pending_user = PendingUser.objects.get(email=email)
        except PendingUser.DoesNotExist:
            return render(request, 'users/invalid_link.html')

        # 使用 PendingUser 中的加密密码创建实际用户
        user = User.objects.create(
            username=email,
            email=email,
            password=pending_user.password,  # 直接使用加密的密码
            is_active=True
        )
        # 激活成功后删除 PendingUser 记录
        pending_user.delete()
    return redirect('/')


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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # 检查是否已经存在待激活用户
            if PendingUser.objects.filter(email=email).exists():
                return render(request, 'users/pending_activation.html')

            # 创建 PendingUser 对象，并加密密码
            pending_user = PendingUser(
                email=email,
                password=make_password(password)  # 使用 make_password 加密密码
            )
            pending_user.save()

            # send email
            send_register_email(form.cleaned_data.get('email'), 'register')
            context = {'form': form}
            return render(request, 'users/activate_account.html', context)

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


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='users:login')   # 登录之后允许访问
def edit_users(request):
    """ 编辑用户信息 """
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    return render(request, 'users/edit_users.html', locals())


def message_profile(request):
    return render(request, 'users/message_profile.html')


@login_required(login_url='users:login')
def followers(request, username):
    target_user = get_object_or_404(User, username=username)
    follower_list = target_user.userprofile.followers.all()

    context = {
        'target_user': target_user,
        'followers': follower_list,
    }

    return render(request, 'users/followers.html', context)


@login_required(login_url='users:login')
def my_followers(request):
    userprofile = request.user.userprofile
    followers = userprofile.followers.all()

    # 获取当前用户的关注状态
    followers_data = []
    for follower in followers:
        is_following = userprofile.following.filter(id=follower.id).exists()
        followers_data.append({
            'username': follower.owner.username,  # 使用 owner 而不是 user
            'image_url': follower.image.url,
            'signature': follower.signature,
            'is_following': is_following
        })

    context = {
        'user': request.user,  # 提供当前用户的信息
        'followers': followers_data,  # 提供粉丝列表及其关注状态
    }

    return render(request, 'users/followers.html', context)


@login_required(login_url='users:login')
def follow_unfollow(request, username):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        action = data.get('action')

        target_user = get_object_or_404(User, username=username)
        userprofile = request.user.userprofile

        # Check if the user is trying to follow themselves
        if request.user == target_user:
            return JsonResponse({'success': False, 'message': 'You cannot follow yourself'}, status=400)

        if action == 'follow':
            if not userprofile.following.filter(id=target_user.userprofile.id).exists():
                userprofile.following.add(target_user.userprofile)
                success = True
                message = f'You are now following {target_user.username}'
            else:
                success = False
                message = f'You are already following {target_user.username}'
        elif action == 'unfollow':
            if userprofile.following.filter(id=target_user.userprofile.id).exists():
                userprofile.following.remove(target_user.userprofile)
                success = True
                message = f'You have unfollowed {target_user.username}'
            else:
                success = False
                message = f'You are not following {target_user.username}'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'}, status=400)

        return JsonResponse({'success': success, 'message': message})

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


@login_required(login_url='users:login')
def other_user_profile(request, username):
    # 获取选中的用户
    selected_user = get_object_or_404(User, username=username)
    # 判断当前用户是否已经关注了这个用户
    is_following = request.user.userprofile.following.filter(id=selected_user.id).exists()
    # 将 selected_user 和 is_following 传递给模板
    return render(request, 'users/other_user_profile.html', {
        'selected_user': selected_user,
        'is_following': is_following
    })
