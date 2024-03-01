from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Turtle
from django.template import loader

def index(request):
    turtles_list = Turtle.objects.all()
    steve = Turtle.objects.get(pk=1)
    template = loader.get_template("controller/index.html")
    context= {
        "turtles_list" : turtles_list,
        "steve" : steve
    }
    return HttpResponse(template.render(context, request))

    # output = ", ".join([t.name for t in turtles_list])
    # return HttpResponse(output)

def detail(request, turtle_name):
    try:
        turtle = Turtle.objects.get(name=turtle_name)
    except Turtle.DoesNotExist:
        raise Http404("Turtle does not exist")
    return render(request, "controller/detail.html", {"turtle": turtle})

def register(request):
    return render(request, "controller/register.html")
