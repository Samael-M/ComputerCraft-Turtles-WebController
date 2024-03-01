from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Turtle
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
import uuid

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
    register_link = str(uuid.uuid4())
    context = {
        "register_link" : register_link
    }
    return render(request, "controller/register.html", context)

def register_turtle(request):
    if request.method == "POST":
        computer = request.POST.get("computerID")
        Turtle.objects.create(name='STEVE', computerID=computer, worldID=0, status=True, position='no')
        return JsonResponse({"status": "registered"})
    return JsonResponse({"error": "Invalid request"}, status=400)