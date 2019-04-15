from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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