from django.shortcuts import render, redirect

from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from .models import  Website, Message

import json
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        return render(request = request,
                        template_name = "chat/home.html")
    return redirect("chat:login_request")

def get_messages(request,link):
    if request.user.is_authenticated:
        if(request.method == 'GET'):
            website = ""
            website_id = ""
            try:    
                website = Website.objects.get(Link=link)
                website_id = website.id
            except:
                website = Website(Link=link)
                website.save()
                website_id = website.id
            messages = Message.objects.filter(website=website)
            message = []
            time = []
            username = []
            print(messages)
            print(len(messages))
            print(request.user.username)
            for m in messages:
                message.append(m.content)
                time.append(str(m.timestamp))
                username.append(m.username)         
            response = json.dumps([{'message':message},{'user':request.user.username},{'time': time},{'id':website_id},{'users':username}])
        return HttpResponse(response, content_type='text/json')
    print("not authenticated")
    return HttpResponse(json.dumps([]), content_type='text/json')

def register(request):
    if request.user.is_authenticated:
        return redirect("chat:home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("chat:home")

        else:
            for msg in form.error_messages:
                print(msg)
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "chat/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "chat/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("chat:login_request")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("chat:home")
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "chat/login.html",
                    context={"form":form})

