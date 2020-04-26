# from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm


def home_page(request):
    """This function returns home_page response"""
    # we can pass something(context) to html template is dictionary
    context = {
        "title": "Home",
        "content": "Please visit our website"
    }
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
    contact_form = ContactForm()
    context = {
        "title": "Contact",
        "content": "Please check our contact information",
        "contact_form": contact_form
    }
    # it is printing data, we got from html
    # accessing frontend data at the backend

    if request.method == "POST":
        # it is dictionary
        print(request.POST)
        print(request.POST.get("fullname"))
        print(request.POST.get("email"))
        print(request.POST.get("content"))
        # print(request.POST.get("name", "No Name"))
        # print(request.POST.get("name"))
        # print(request.POST["name"])
    return render(request, "contact/view.html", context)
