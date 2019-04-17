from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next= 정의되어 있으면 
            return redirect(request.GET.get('next') or 'posts:list')
        return redirect('accounts:login')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
        


def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
    
def signup(request):
    # POST: 유저 등록
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
        return redirect('accounts:signup')
    # GET: 유저 정보 입력
    else:
        form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
        
        
def people(request, username):
    # 사용자에 대한 정보
    person = get_object_or_404(get_user_model(), username=username)
    # 1. settings.AUTH_USER_MODEL(django.conf)
    # 2. get_user_model()(django.contrib.auth) - 쓸 것
    # 3. User(django.contrib.auth.models) - 쓰지 말 것
    return render(request, 'accounts/people.html', {'person': person})
    
    
# 회원 정보 변경(편집, 반영)
def update(request):
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('people', user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 1. instance 넣어줄 정보가 있는 User가 있고 없는 User도 있다.
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
        context = {
            'user_change_form': user_change_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/update.html', context)
        
        
def delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('posts:list')
    return render(request, 'accounts/delete.html')
    
    
def password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
        context = {
            'password_change_form': password_change_form,
        }
        return render(request, 'accounts/password.html', context)