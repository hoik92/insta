from django.shortcuts import render, redirect
from .forms import PostModelForm
from .models import Post

# Create your views here.


def create(request):
    if request.method == 'POST':
        # 작성된 post를 DB에 적용
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('posts:create')
    else:
        # post를 작성하는 form을 보여줌
        form = PostModelForm()
        return render(request, 'posts/create.html', {'form': form})
        
