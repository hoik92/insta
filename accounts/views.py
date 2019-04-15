from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

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