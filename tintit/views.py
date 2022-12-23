import re

from operator import contains
from sqlite3 import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
import json

from .models import User, Wallpapers

class CreateWallpaper(forms.Form):
    title = forms.CharField(label="Title", max_length=50, widget=forms.TextInput(attrs={"autofocus": "autofocus", "class": "form-control", "id": "form-title"}))
    desc = forms.CharField(label="Description", max_length=160, required=False, widget=forms.Textarea(attrs={"rows": 4, "cols": 50, "class": "form-control"}))
    file_img = forms.ImageField(label="", required=False)
    url_img = forms.URLField(label="", required=False, widget=forms.Textarea(attrs={"placeholder": "Image url (optional)", "rows": 2, "cols": 50, "class": "form-control"}))
    allow_comments = forms.BooleanField(initial=True)

    
# Create your views here.
def shapeatint(request):
    if request.method == "POST":
        form = CreateWallpaper(request.POST, request.FILES)
        if form.is_valid():
            stdrValidResolutions = [16/9, 4/3]
            isValid = False
            modelForm = Wallpapers()
            modelForm.user = request.user

            # Check chosen image importation method by user:
            
            # by file and url -> get only file
            if form.cleaned_data["file_img"] != None and len(str(form.cleaned_data["url_img"])) > 0:
                modelForm.file_img = form.cleaned_data["file_img"]

            # by no file nor url -> redirect back to form
            elif form.cleaned_data["file_img"] == None and len(str(form.cleaned_data["url_img"])) <= 0:
                form = CreateWallpaper()
                return render(request, "tintit/shapeatint.html", {
                    "form": form
                })

            # by file but not url -> get only file
            elif form.cleaned_data["file_img"] and len(str(form.cleaned_data["url_img"])) <= 0:
                modelForm.file_img = form.cleaned_data["file_img"]

            # by no file but url -> get only the url
            elif form.cleaned_data["file_img"] == None and len(str(form.cleaned_data["url_img"])) >= 0:
                modelForm.url_img = form.cleaned_data["url_img"]

            if modelForm.file_img:
                importedImageResolution = int(modelForm.file_img.height)/int(modelForm.file_img.width)

                # Check if user's image resolution is valid
                for stdrValidResolution in stdrValidResolutions:
                    if stdrValidResolution == importedImageResolution:
                        isValid = True

            modelForm.title = form.cleaned_data["title"]
            modelForm.desc = form.cleaned_data["desc"]
            modelForm.allow_comments = form.cleaned_data["allow_comments"]
            modelForm.save()
            messages.add_message(request, messages.INFO, form)
            return redirect("index")
        else:
            form = CreateWallpaper()
            return render(request, "tintit/shapeatint.html", {
                "form": form
            })
    form = CreateWallpaper()
    return render(request, "tintit/shapeatint.html", {
        "form": form
    })

def index(request):
    wallpapers = Wallpapers.objects.all()
    return render(request, "tintit/index.html", {
        "wallpapers": wallpapers
    })

def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tintit/login.html", {
                "message": "Invalid username and/or password"
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "tintit/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if len(username) > 20:
            return render(request, "tintit/register.html", {
                "message": "Username should be 20 characters or fewer. Letters, digits and @/./+/-/_ only."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tintit/register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tintit/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tintit/register.html")