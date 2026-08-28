from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Registration View
def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # don't save it to the database yet.
            # Because you need to process the password first.
            user = form.save(commit=False)
            # set_password() converts it into a secure hash.
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request,'Registration fail, please correct the error below.')
    else:
        form = RegisterForm()
    return render(request,"accounts/register.html",{"form": form})

# Login View
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect("dashboard")
        else:
            messages.error(request,'Invalid username and password')

    return render(request,"accounts/login.html")

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect("login")
