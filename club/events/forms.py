from django import forms
from django.forms import ModelForm
from .models import Training, Exercise, TrainingExercise, Comment
from django.utils.safestring import mark_safe



class HorizontalRadioRenderer(forms.RadioSelect):
   def render(self):
     return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class DateInput(forms.DateInput):
    input_type = "date"

class TrainingForm(ModelForm):            
    # exercises = forms.ModelMultipleChoiceField(queryset = Exercise.objects.all())
    # ^ to bedzie w TrainingExerciseForm
         
       
    class Meta:
        model = Training
        exclude = {"user","date_created"}
        widgets = {
            "date": DateInput(),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Push/Pull/Legs/Full body'}),
            'description' : forms.Textarea(attrs={"rows": 3}),
            'show_to' :  forms.RadioSelect(attrs={'class': 'form-check-inline'})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

    
        if not(name[0].isupper()):
            self.add_error('name','Name must starts with a capital letter') 


class TrainingExerciseForm(ModelForm):
    exercise = forms.ModelChoiceField(queryset = Exercise.objects.all())
    class Meta:
        model = TrainingExercise
        fields = ['sets','reps','weight','unit','exercise']
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
        
        
        
        
        

    
        