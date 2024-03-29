from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username



class Category(models.Model):
    title= models.CharField(max_length=25)

    def __str__(self):
        return self.title



class Post(models.Model):
    title = models.CharField(max_length=150)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    #comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'id': self.id
        })
