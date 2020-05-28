# from django.http import HttpResponse
from django.shortcuts import render


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
    context = {
        "title": "Contact",
        "content": "Please check our contact information"
    }
    return render(request, "contact_page.html", context)
