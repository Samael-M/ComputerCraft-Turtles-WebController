from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta
import uuid
import json

from .models import Token, Turtle

def create_token(hours, minutes, seconds):
    time = timezone.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return Token.objects.create(id=uuid.uuid4(), date=time)


class TokenModelTests(TestCase):
    """
    Testing that Token.expired() works
    """
    def test_new_token_not_expired(self):
        token = create_token(hours=0, minutes=0, seconds=0)
        self.assertFalse(token.expired())

    def test_token_not_expired(self):
        token = create_token(hours=0, minutes=-59, seconds=-59)
        self.assertFalse(token.expired())

    def test_token_expired(self):
        token = create_token(hours=-1, minutes=0, seconds=-1)
        self.assertTrue(token.expired())

class RegistrationTests(TestCase):
    """
    Testing registration process
    """
    def test_registration_expired_token(self):
        """
        Request to register with an expired token are rejected and token is deleted. Response status=400, error: Token has expired!
        """
        token = create_token(hours=-1, minutes=0, seconds=-1)
        url = reverse("controller:register_turtle", kwargs={"register_link": token.id})
        response = self.client.post(url)

        token_cleared = not Token.objects.filter(id=token.id).exists()
        self.assertTrue(token_cleared)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "Token has expired!"})

    def test_registration_invalid_token(self):
        """
        Request to register with an invalid token are rejected. Response status=400, error: Invalid token!
        """
        token = uuid.uuid4()
        url = reverse("controller:register_turtle", kwargs={"register_link": token})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "Invalid token!"})
    

    def test_registration_duplicate_ID(self):
        """
        Request to registe an already registered bot are rejected and token is deleted. Response status=409, error: This turtle is already registered!
        """
        token = create_token(hours=0, minutes=0, seconds=0)
        hsData = {
            "name": "ExampleName",
            "computerID": 1234,
            "worldID": 1234,
            "status": True,
        }
        
        #initate handshake 
        url = reverse("controller:register_turtle", kwargs={"register_link": token.id})
        handshake = self.client.post(url, data=json.dumps(hsData), content_type='application/json')
        self.assertEqual(handshake.status_code, 200)

        responseData = json.loads(handshake.content.decode('utf-8'))
        turtleID = responseData["serverID"]
        Turtle.objects.create(id=turtleID, name=hsData['name'], worldID=hsData['worldID'], computerID=hsData['computerID'], status=hsData['status'])

        #finalize registration
        idData = {
            "serverID": turtleID,
        }
        response = self.client.post(url, data=json.dumps(idData), content_type='application/json')

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error":"This turtle is already registered!", "type":"serverID duplicate"})

        token_cleared = not Token.objects.filter(id=token.id).exists()
        self.assertTrue(token_cleared)
    
    def test_registration_duplicate_worldcomputer(self):
        """
        Request to registe an already registered bot are rejected and token is deleted. Response status=409, error: This turtle is already registered!
        """
        token = create_token(hours=0, minutes=0, seconds=0)
        data = {
            "serverID": "",
            "name": "ExampleName",
            "computerID": 1234,
            "worldID": 1234,
            "status": True,
        }
        Turtle.objects.create(id=uuid.uuid4(), name=data['name'], worldID=data['worldID'], computerID=data['computerID'], status=data['status'])

        #initate handshake 
        url = reverse("controller:register_turtle", kwargs={"register_link": token.id})
        handshake = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(handshake.status_code, 200)

        responseData = json.loads(handshake.content.decode('utf-8'))
        data["serverID"] =  responseData["serverID"]

        #finalize registration
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error":"This turtle is already registered!", "type":"world and computer ID duplicate"})

        token_cleared = not Token.objects.filter(id=token.id).exists()
        self.assertTrue(token_cleared)

    def test_registration_accepted(self):
        """
        Request to register with a valid token are accepted. Token is deleted and turtle is added to database. 
        Response Status=200 and body contains an ID for the turtle
        """
        token = create_token(hours=0, minutes=0, seconds=0)
        data = {
            "server": "",
            "name": "ExampleName",
            "computerID": 1234,
            "worldID": 1234,
            "status": True,
        }

        #initate handshake 
        url = reverse("controller:register_turtle", kwargs={"register_link": token.id})
        handshake = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(handshake.status_code, 200)

        responseData = json.loads(handshake.content.decode('utf-8'))
        data["serverID"] =  responseData["serverID"]

        #finalize registration
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        turtle_registered = Turtle.objects.filter(id = data["serverID"], computerID = data['computerID'], worldID = data['worldID'])
        self.assertTrue(turtle_registered)

        token_cleared = not Token.objects.filter(id=token.id).exists()
        self.assertTrue(token_cleared)

#   TEST REGISTRATION WHERE HANDSHAKE WORKS BUT REPONSE HAS WRONG ID