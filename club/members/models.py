from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    
    phone = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(null = True, blank=True)
    email = models.CharField(max_length=100,null=True, blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def get_unfollow_url(self):
        return reverse('unfollow', kwargs={'username': self.username})
        

    def get_follow_url(self):
        return reverse('follow', kwargs={'username': self.username})
        
    
    def get_profile_url(self):
        return reverse('profile', kwargs={'username': self.username})
    
    
    def change_username(self):
        self.user.username = self.username
        
    
    def change_email(self):
        self.user.email = self.email
        
    # def get_userprofile_followers(self):
    #     return self.get_userprofile_followers.all()
    
    
    def __str__(self):
        return self.username
    
    
    
    
    

    
    