from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next= 정의되어 있으면 
            return redirect(request.GET.get('next') or 'posts:list')
        else:
            return redirect('accounts:login')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
        


def logout(request):
    auth_logout(request)
    return redirect('posts:list')