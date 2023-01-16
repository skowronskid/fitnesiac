from django.contrib import admin
from .models import Training, Exercise, TrainingExercise
# Register your models here.

    
class TrainingExerciseInLine(admin.StackedInline):
    model = TrainingExercise
    extra = 1
    readonly_fields = ['as_mks', 'as_imperial']
    
@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    inlines = [TrainingExerciseInLine]
    # fields = ('name','date','start_time','end_time','user')
    readonly_fields = ['duration']
    list_display = ("date","user","name")
    ordering = ('-date',) 
    
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    fields = ('name','bodyPart','equipment','gifUrl','target')
    list_display = ("target","bodyPart","name")
    ordering = ('target',) 
    
