"""This is views module, it handled website views"""
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
    """This function returns home_page response"""
    # we can pass something(context) to html template is dictionary
    context = {
        "title": "Home",
        "content": "Please visit our website",
    }
    if request.user.is_authenticated():
        context["premium_content"] = "YAHOO"
    return render(request, "home_page.html", context)


def about_page(request):
    """This function returns about_page response"""
    context = {
        "title": "About",
        "content": "Please give feedback of our website"
    }
    return render(request, "about_page.html", context)


def contact_page(request):
    """This function returns contact_page response"""
    # print("Request is: ", request)
    contact_form = ContactForm(request.POST or None)
    # print(contact_form.is_bound)
    context = {
        "title": "Contact",
        "content": "Please check our contact information",
        "contact_form": contact_form,
        "brand": "New Brand Name"
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, "contact/view.html", context)


def login_page(request):
    """Implements user login functionality"""
    # Session.objects.all().delete()
    login_form = LoginForm(request.POST or None)
    context = {
        "login_form": login_form
    }
    print("User Logged In : ")
    print(request.user.is_authenticated())
    print(request.user)
    if login_form.is_valid():
        print(login_form.cleaned_data)
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)
            # context["login_form"] = LoginForm()
            # it will go to home_page
            return redirect("/")
        else:
            print("Error")
        # print(login_form.cleaned_data)
    Session.objects.all().delete()
    return render(request, "auth/login.html", context)


# user is created
User = get_user_model()


def register_page(request):
    """Implements user register functionality"""
    register_form = RegisterForm(request.POST or None)
    context = {
        "register_form": register_form
    }
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username = register_form.cleaned_data.get("username")
        email = register_form.cleaned_data.get("email")
        password = register_form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print("User is: ", new_user)

    return render(request, "auth/register.html", context)
