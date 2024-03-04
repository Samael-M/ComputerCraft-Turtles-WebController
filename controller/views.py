from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Turtle
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import uuid
import json

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

@csrf_exempt
def register_turtle(request, register_link):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        computer = data.get("computerID")
        Turtle.objects.create(name='STEVE2', worldID=0, computerID=computer, status=True, position='no')
        return JsonResponse({"status": "registered"})
    return JsonResponse({"error": "Invalid request"}, status=400)