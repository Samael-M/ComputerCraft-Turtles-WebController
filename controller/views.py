from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction

import uuid
import json

from .models import Turtle, Token

"""
Main view/home page. Links to detail view for bots and to the registration page
"""
def index(request):
    turtles_list = Turtle.objects.all()
    context = {
        "turtles_list": turtles_list
    }
    template = loader.get_template("controller/index.html")
    return HttpResponse(template.render(context, request))

"""
View details of a particular bot
"""
def detail(request, turtle_name):
    try:
        turtle = Turtle.objects.get(name=turtle_name)
    except Turtle.DoesNotExist:
        raise Http404("Turtle does not exist")
    return render(request, "controller/detail.html", {"turtle": turtle})

"""
Regisration page. Used to generate registration codes for user 
"""
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

"""
Not a viewable  link, handles registration request from bots
"""
@csrf_exempt
@transaction.atomic
def register_turtle(request, register_link):
    if request.method == "POST":
        try:
            token = Token.objects.get(id=register_link)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Invalid token!"}, status=400)
        
        if(not token.expired()):
            data = json.loads(request.body.decode('utf-8'))
            
            serverID = data.get("serverID")
            if(not serverID):
                serverID = str(uuid.uuid4())
                request.session['id'] = serverID
                return JsonResponse({"serverID": serverID}, status=200)
            else:
                sentID = request.session.pop('id', None)
                if(serverID != sentID):
                    token.delete()
                    return JsonResponse({"error": "Reponse does not have proper ID"}, status=400)
                
                computer = data.get("computerID")
                world = data.get("worldID")
                if(Turtle.objects.filter(id=serverID).exists()):
                    token.delete()
                    return JsonResponse({"error":"This turtle is already registered!", "type":"serverID duplicate"}, status=409)
                elif(Turtle.objects.filter(worldID=world, computerID=computer).exists()):
                    token.delete()
                    return JsonResponse({"error":"This turtle is already registered!", "type":"world and computer ID duplicate"}, status=409)
                
                name = data.get("name")
                stat = data.get("status")

                token.delete()
                Turtle.objects.create(id = serverID, name=name, worldID=world, computerID=computer)
                return JsonResponse({"status": "You are now registered with the web server!"}, status=200)
        else:
            token.delete()
            return JsonResponse({"error": "Token has expired!"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)