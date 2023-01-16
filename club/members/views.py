from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from events.models import Training
from .models import UserProfile
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm, SettingsForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Create your views here.

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
            if  user.is_active == 0:
                return render(request,'authenticate/login.html',context={"message" :"You have not activated your account, check your email inbox."})
        except:
            return render(request,'authenticate/login.html',context={"message" :"There is no account with such username"})
    
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'authenticate/login.html',context={"message" :"Incorrect password"})
                
            
    else:
        return render(request, 'authenticate/login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("You were logged out"))
    return redirect('home')




def register_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # profile_form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            UserProfile.objects.create(
                user = user,
                email = user.email,
                username = user.username,
                photo = 'default.png'
            )
            
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authenticate/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            context = {
                'login_message' : "You can login after you have confirmed your account. \n Check your email inbox (the message might be in spam folder). "
            }
            return render(request, 'authenticate/login.html', context =  context)
    else:
        form = SignupForm()
    return render(request, 'authenticate/register_user.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return redirect('login')
    
    
def view_profile(request,username=None):
    user = User.objects.get(username=username)
    trainings = Training.objects.filter(user = user)
    userprofile = UserProfile.objects.get(username = username)
    context = {
        "username" : request.user.username,
        "trainings" : trainings,
        "userprofile" : userprofile,
        "in_card" : True
    }
    return render(request, 'profile/profile.html', context)


def change_user_settings(request):
    obj = get_object_or_404(UserProfile, user=request.user)
    user = User.objects.get(username = request.user.username)
    
    
    form = SettingsForm(instance=obj)
    
    if form.is_valid():
        form.save()
        # context['message'] = "Data saved."
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES,instance=obj)
        if form.is_valid():
            profile = form.save()
            user.username = profile.username
            user.email = profile.email
            user.save()
            return redirect(reverse('profile', kwargs={"username":request.user.username}))

        
    return render(request, 'profile/settings.html', {'form': form})


def follow_user(request, username=None):
    userprofile = request.user.userprofile
    userprofile.follows.add(UserProfile.objects.get(username=username)) 
    userprofile.save()
    if request.htmx:       
        return render(request, "profile/partials/unfollow.html")
    return HttpResponse("Added")


def unfollow_user(request,username=None):
    userprofile = request.user.userprofile
    userprofile.follows.remove(UserProfile.objects.get(username=username)) 
    userprofile.save()
    if request.htmx:
        return render(request, "profile/partials/follow.html")
    return HttpResponse("Removed")
    
    