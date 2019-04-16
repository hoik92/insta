from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Post(models.Model):
    content = models.CharField(max_length=150)
    image = models.ImageField(blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts", blank=True)
    
    def __str__(self):
        return f"{self.id}: {self.content}"
        
        
class Comment(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content