from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile

def registration(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            avatar = request.FILES.get("avatar")

            profile = Profile.objects.create(user=user)
            profile.avatar.save(avatar.name, avatar)

            login(request, user)
            return redirect("/")

    return render(request, 'registration/register.html', {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
            avatar = request.FILES.get("avatar")
    
            profile = request.user.profile
            profile.avatar.save(avatar.name, avatar)
    
    return render(request, "registration/profile.html")
