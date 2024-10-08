from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length = 75)
  subtitle = models.CharField(max_length = 100)
  content = models.TextField()
  date_posted= models.DateTimeField(default = timezone.now)
  author = models.ForeignKey(User, on_delete = models.CASCADE)

  def __str__(self):
    return self.title
  
  # Returns the url (with the pk) of the post-detail view
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
  
  def total_likes(self):
    return self.likes.count()
  
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # Each unique user can only like each post once
    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'