from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Turtle
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    turtles_list = Turtle.objects.all()
    context = {
        "turtles_list": turtles_list
    }
    template = loader.get_template("controller/index.html")
    return HttpResponse(template.render(context, request))


def detail(request, turtle_name):
    try:
        turtle = Turtle.objects.get(name=turtle_name)
    except Turtle.DoesNotExist:
        raise Http404("Turtle does not exist")
    return render(request, "controller/detail.html", {"turtle": turtle})

def register(request):
    return render(request, "controller/register.html")
