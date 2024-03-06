from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import uuid
import json

from .models import Turtle, Token


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
    if(request.method == "POST"):
        register_code = str(uuid.uuid4())
        Token.objects.create(id=register_code, date=timezone.now())
        request.session['code'] = register_code
        return redirect('controller:register')
    else:
        register_code = request.session.pop('code', None)

    context = {
        "code":register_code
    }
    return render(request, "controller/register.html", context)

@csrf_exempt
def register_turtle(request, register_link):

    if request.method == "POST":
        token = Token.objects.get(id=register_link)
        if(token and not token.expired()):
            data = json.loads(request.body.decode('utf-8'))
            serverID = str(uuid.uuid4())

            compName = data.get("name")
            computer = data.get("computerID")
            world = data.get("worldID")
            stat = data.get("status")
            pos = data.get("position")

            # django.db.utils.IntegrityError: NOT NULL constraint failed: controller_turtle.name
            #Turtle.objects.create(id = serverID, name=compName, worldID=world, computerID=computer, status=stat, position=pos)
            token.delete()
            return JsonResponse({"id": serverID})   
        else:
            return JsonResponse({"error": "Invalid token!"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

#curl -X POST http://localhost:8000/controller/register// -H "Content-Type: application/json" \ -d '{"name":"TestBot2", "computerID":"12234", "worldID":0, "status":True, "position":"0,0,0"}'