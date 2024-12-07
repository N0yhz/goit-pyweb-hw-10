from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request, f"Account created for {username}!")
                return redirect('users:login')
            else:
                messages.error(request,"user authentication failed")
        else:
            messages.error(request, "There was a problem with your registration")
    else:
        form=UserCreationForm()
    return render(request, 'users/register.html', {
        'form': form,
    })

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quotes:root')
        else:
            messages.success(request, ("There was an error loggin in, try again") )
            return redirect('users:login')
    else:
        return render(request, 'users/login.html', {} )
    
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!!") )
    return redirect('users:login')