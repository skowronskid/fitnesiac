import pint
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from datetime import datetime,  date, timedelta

ZERO = timezone.timedelta(0)


class Exercise(models.Model):
    bodyPart = models.CharField('Body Part',max_length=120, null=True, blank=True)
    equipment = models.CharField('Equipment',max_length=120, null=True, blank=True)
    gifUrl = models.CharField('Gif URL',max_length=500, null=True, blank=True)
    target = models.CharField('Name',max_length=300, null=True, blank=True) # pamiętać, że name to target z jakeigos powodu xd
    name = models.CharField('Target',max_length=120, null=True, blank=True)

    def __str__(self):
        return self.target
 
def default_start_time():
    # a callable so that it doesn't update database each time makemigrations is made
    return datetime.now()- timedelta(minutes=90)
     

class Training(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    
    name = models.CharField('Training name', max_length=150, blank=False, null=False)
    date = models.DateField()
    start_time = models.TimeField(default=default_start_time ) 
    end_time = models.TimeField(default=datetime.now)
    description = models.CharField(max_length=500, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    show_to = models.CharField("Who can view this training:", choices=(
        ('2', "everyone" ),
        ("1", "my followers"),
        ("0", "only me") 
        ), default=1, null=True, max_length=10)    

    def get_edit_url(self):
        return reverse('update', kwargs={'id': self.id})
    
    def get_delete_url(self):
        return reverse('delete', kwargs={'id': self.id})
    
    
    def get_exercises_children(self):
        return self.trainingexercise_set.all()
    
        
    def get_comments_children(self):
        return self.comment_set.all()
    
    def has_comments(self):
        return self.comment_set.count() > 0
    
    def duration(self):
        return datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time) #weird but works 
    
    def __str__(self) -> str:
        return self.name
    
    

# test


class TrainingExercise(models.Model):
    
    #zrobi się, żeby po wybraniu ćwiczeń pojawiało się nowy form do każdego ćwiczenia, każdy form jest połaczony kluczem trainig z treningiem 
    training = models.ForeignKey(Training, on_delete=models.CASCADE,blank=True, null=True)
    
    # plan na exercise jest, żeby łączyć z listą exercises
    exercise = models.ForeignKey(Exercise, on_delete=models.DO_NOTHING,blank=True, null=True) # jeśli się usunie z bazy dane ćwiczenie to tu się nic nie zmieni (czemu usuwać ćwiczenie z bazy?)
    
    weight = models.FloatField("Weight")
    unit = models.CharField(max_length=10, choices=[("pounds","pounds"),("kilogram","kilogram")], default="kilogram")
    sets = models.IntegerField('Nr of sets',choices = [(i,i) for i in range(1,11)],blank=False,null=False)
    reps = models.IntegerField('Nr of reps in a set', choices = [(i,i) for i in range(1,20)], blank=False,null=False)
    
    def get_edit_url(self):
        kwargs = {
            "parent_id" : self.training.id,
            "id":self.id
        }
        return reverse("exercise-update",kwargs = kwargs)
    
    def get_delete_url(self):
        kwargs = {
            "parent_id" : self.training.id,
            "id":self.id
        }
        return reverse("exercise-delete",kwargs = kwargs)
    
    
    def convert(self,system="mks"):
        if self.weight is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.weight * ureg[self.unit]
        return measurement
    
    def as_mks(self):
        measurement = self.convert(system='mks')
        return measurement.to('kilogram')
        
    def as_imperial(self):
        measurement = self.convert(system='imperial')       
        return measurement.to('pounds')
    
    
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    training = models.ForeignKey(Training,on_delete=models.CASCADE,blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now = True, null=True)
    text = models.TextField(max_length=500)
    

    
    def get_edit_url(self):
        kwargs = {
            "parent_id" : self.training.id,
            "id":self.id
        }
        return reverse("comment-update",kwargs = kwargs)
    
    def get_delete_url(self):
        kwargs = {
            "parent_id" : self.training.id,
            "id":self.id
        }
        return reverse("comment-delete",kwargs = kwargs)
    
    
    
            
    
    
    
    
