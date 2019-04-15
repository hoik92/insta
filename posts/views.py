from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostModelForm
from .models import Post

# Create your views here.


def create(request):
    if request.method == 'POST':
        # 작성된 post를 DB에 적용
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
        return redirect('posts:create')
    else:
        # post를 작성하는 form을 보여줌
        form = PostModelForm()
        return render(request, 'posts/create.html', {'form': form})
        
        
def list(request):
    # 모든 Post를 보여줌
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})
    
    
def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
        
    post.delete()
    return redirect('posts:list')


def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
        return redirect('posts:update')
    else:
        form = PostModelForm(instance=post)
        return render(request, 'posts/create.html', {'form': form})
        
        
def like(request, post_id):
    # 1. like를 추가할 포스트를 가져옴
    post = get_object_or_404(Post, id=post_id)
    # 2. 만약 유저가 해당 post를 이미 like 했다면
    #   like를 제거하고
    # 아니면
    #   like를 추가한다.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')