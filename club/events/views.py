from django.shortcuts import render, redirect,get_object_or_404
import calendar
from calendar import HTMLCalendar
from django.urls import reverse, reverse_lazy
from datetime import datetime
from .models import Exercise, Training, TrainingExercise, Comment
from .forms import TrainingForm, TrainingExerciseForm, CommentForm
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
from members.models import UserProfile
from django.core import serializers
import requests


@login_required
def api_view(request):
    data = Training.objects.all()
    training_name = request.GET.get('training_name')
    training_date = request.GET.get('training_date')

    ## TODO dodać stronkę z formularzem i tu przechwytywać odpowiedzi
    if training_name != '' and training_name is not None:
        data = data.filter(name__icontains=training_name)

    if training_date != '' and training_date is not None:
        data = data.filter(date=training_date)

    data = serializers.serialize('json', data)
    return HttpResponse(data, content_type="application/json")
    # if request.headers['Content-Type'] == 'application/json': 
    # return JsonResponse(data, safe=False)

    # elif request.headers['Content-Type'] == 'application/xml':
    # xml = serializers.serialize('xml', data)
    # return HttpResponse(xml, content_type='application/xml')


def trainings_view(request):
    trainings = Training.objects.all()
    context = {'trainings': trainings}
    xml = render_to_string('events/trainings.xml', context)
    return HttpResponse(xml, content_type='application/xml')

# view do wyswietlania treningow potem
@login_required
def list_trainings(request): 
    
    # getting user's follows
    userprofile = UserProfile.objects.get(user=request.user)
    follows = userprofile.follows.all().values_list('user', flat=True) # to jest to
    follows = list(follows)
    follows.append(request.user.id) #appending request user so that he sees his own posts
    
    
    # shows trainigs of people that an user follows and the ones that everybody sees
    queryset = Training.objects.filter(Q(show_to='2')| Q(show_to='1', user_id__in = follows )).order_by('-date_created')
    context = {
        "training_list" : queryset,
        "in_card" : True
    }
    return render(request, "events/trainings.html", context)


# view do wyswietlania  detali treningow potem
@login_required
def view_training_details(request, id=None):
    # training details in a static form
    url = reverse("details",kwargs={"id": id})
    context = {
        "url" : url
        }
    return render(request, "events/partials/detail.html",context)
    

@login_required
def add_training(request):
    # new training instance, redirects to update trainig after submiting in order to add exercises
    submitted = False 
    if request.method == "POST":
        print('tu')
        form = TrainingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(reverse('update', kwargs={"id":obj.id,}))
        
    else:
        form = TrainingForm
        if 'submitted' in request.GET:
            submitted = True
         
    return render(request,'events/add_training.html',{'form':form,'submitted':submitted})



@login_required
def update_training(request,id=None):
    obj = get_object_or_404(Training, id=id, user=request.user)
    form = TrainingForm(request.POST or None, instance=obj)

    new_exercise_url = reverse('exercise-add', kwargs = {"parent_id":obj.id})

    context = {
        "form": form,
        "object" : obj,
        "new_exercise_url" : new_exercise_url
    }
    if form.is_valid():
        form.save()
        context['message'] = "Data saved."
        return render(request, "events/partials/detail.html",context)
        
    if request.htmx:
        return render(request, "events/partials/forms.html",context)
    return render(request, "events/update_training.html",context)



@login_required
def update_exercise(request, parent_id = None, id=None):
    # update exercise in past/new training
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Training.objects.get(id = parent_id, user=request.user)

    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found")
        
    
    instance = None
    if id is not None:
        try:
            instance = TrainingExercise.objects.get(id=id)
        except:
            instance = None
        
    print(request.method) #dlaczego tu jest get, tak powinno być?
    url = instance.get_edit_url() if instance else reverse('exercise-add', kwargs = {"parent_id":parent_obj.id})
    
    form = TrainingExerciseForm(request.POST or None, instance=instance)

    context = {
        "url" : url,
        "form" : form, 
        "object" : instance
    }

    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.training = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "events/partials/exercise-inline.html",context)
    return render(request, "events/partials/exercise-form.html",context)



def all_exercises(request):
    # view all exercises and filter them
    exercise_list = Exercise.objects.all()
    exercise_name_query = request.GET.get('exercise_name')
    exercise_bodyPart_query = request.GET.get('exercise_bodyPart')
    exercise_equipment_query = request.GET.get('exercise_equipment')
    

    if exercise_name_query != '' and exercise_name_query is not None:
        exercise_list = exercise_list.filter(target__icontains=exercise_name_query)

    if exercise_bodyPart_query != '' and exercise_bodyPart_query is not None:
        exercise_list = exercise_list.filter(bodyPart=exercise_bodyPart_query)

    if exercise_equipment_query != '' and exercise_equipment_query is not None:
        exercise_list = exercise_list.filter(equipment=exercise_equipment_query)

    context = {
        'exercise_list':exercise_list
    }
    return render(request,'events/exercise_list.html',context)

   
class HTTPResponseHXRedirect(HttpResponseRedirect):
    # reload whole page 
    # used after deletion to go back to list-trainings
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect']=self['Location']
    status_code = 200   


def delete_training(request, id = None):
    # deletes training from database
    try:
        obj = Training.objects.get(id=id, user=request.user)
    except:
        obj = None
       
    if obj is None:
       
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404

    if request.method == "POST":
        obj.delete()
        if request.htmx:
            return HTTPResponseHXRedirect(redirect_to=reverse("list-trainings"))
        return redirect('list-trainings')

        
    context = {
        "object" : obj
    }
    return render(request, 'events/delete.html', context)


def delete_exercise(request, parent_id = None, id = None):
    # deletes training from database
    try:
        obj = TrainingExercise.objects.get(training_id = parent_id,id=id)
    except:
        obj = None
    if obj is None:
       
        if request.htmx:

            return HttpResponse("Not Found")
        raise Http404

    if request.method == "POST":
        name = obj.exercise
        obj.delete()
        success_url = reverse('update', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "events/partials/exercise-inline-delete-response.html", {"name": name})
        return redirect(success_url)

        
    context = {
        "object" : obj
    }
    return render(request, 'events/delete.html', context)


@login_required



def add_comment(request, parent_id=None):

    try:
        parent_obj = Training.objects.get(id=parent_id)        
    except:
        parent_obj = None
    if parent_obj is None:
        
        return HttpResponse("Not found")

    form = CommentForm(request.POST or None)
    
    url = reverse("comment-add", kwargs={"parent_id": parent_obj.id})
    context = {"url": url, "form": form}
    if form.is_valid():
        print('tu4')
        
        new_obj = form.save(commit=False)
        new_obj.training = parent_obj
        new_obj.user = request.user
        new_obj.save()
        context["object"] = new_obj
        print('tu5')
        
        return render(request, "events/partials/comment-inline.html", context)
    print('tu6')
    
    return render(request, "events/partials/comment-form.html", context)


@login_required
def update_comment(request, parent_id = None, id=None):
    # updates a comment in training
    try:
        parent_obj = Training.objects.get(id = parent_id)

    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found")
        
    
    instance = None
    if id is not None:
        try:
            instance = Comment.objects.get(id=id)
        except:
            instance = None
        
    
    url = instance.get_edit_url() if instance else reverse('comment-add', kwargs = {"parent_id":parent_obj.id})
    
    form = CommentForm(request.POST or None, instance=instance)

    context = {
        "url" : url,
        "form" : form, 
        "object" : instance
    }

    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.training = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "events/partials/comment-inline.html",context)
    return render(request, "events/partials/comment-form.html",context)



def delete_comment(request, parent_id = None, id = None):
    # deletes a comment in training
    try:
        obj = Comment.objects.get(training_id = parent_id,id=id)
    except:
        obj = None
    if obj is None:
       
        if request.htmx:

            return HttpResponse("Not Found")
        raise Http404

    if request.method == "POST":
        obj.delete()
        success_url = reverse('update', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "events/partials/comment-inline-delete-response.html")
        return redirect(success_url)

        
    context = {
        "object" : obj
    }
    return render(request, 'events/delete.html', context)

def comments_toggle(request, object_id=None):
    if not request.htmx:
        print('tu')
        raise Http404
    return HttpResponse('')


def search_profiles(request):
    context = {}
    if request.method == "POST":
        searched = request.POST['searched']
        userprofiles = UserProfile.objects.filter(username__contains=searched)
        context["searched"] = searched
        context["userprofiles"] = userprofiles
        return render(request,'events/search_profiles.html',context)
    else:
        return render(request,'events/search_profiles.html')
        



def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    month = month.title()
    month_number = int(list(calendar.month_name).index(month))

    cal = HTMLCalendar().formatmonth(year,month_number)
    now = datetime.now()
    current_year = now.year
    time = now.strftime('%I:%M:%S %p')

    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # if x_forwarded_for:
    #    ip = x_forwarded_for.split(',')[0]

    # else:
    #    ip = request.META.get('REMOTE_ADDR')

    # activity = 'skiing'
    # api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(activity)
    # response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
    # if response.status_code == requests.codes.ok:
    #     text = response.text
    # else:
    #     text = "Error:"+str(response.status_code)+str(response.text)

    return render(request,'events/home.html',
    {
        "year":year,
        "month":month,
        "month_number": month_number,
        "cal":cal,
        "current_year":current_year,
        "time":time,
        # "ip":ip,
        # "text":text,
    })