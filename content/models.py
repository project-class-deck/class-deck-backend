from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Board(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    introduction = models.TextField()
    members = models.ManyToManyField(User, related_name='boards')
    access_code = models.CharField(max_length=7, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    categories = models.ManyToManyField('Category', related_name='boards')
    is_subscription_based = models.BooleanField(default=False)

class Category(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)

class Post(models.Model):
    title = models.CharField(max_length=255)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.ManyToManyField('Comment', related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
class BoardMembershipRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_requests')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='membership_requests')
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'board')  # 각 사용자는 각 보드에 대해 하나의 가입 신청만 가능