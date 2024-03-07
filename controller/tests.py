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

    ####################################
        
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
    
    def test_registration_duplicate(self):
        """
        Request to registe an already registered bot are rejected and token is deleted. Response status=409, error: This turtle is already registered!
        """
        token = create_token(hours=0, minutes=0, seconds=0)
        data = {
            "name": "ExampleName",
            "computerID": 1234,
            "worldID": 1234,
            "status": True,
        }
        Turtle.objects.create(id=uuid.uuid4(), name=data['name'], worldID=data['worldID'], computerID=data['computerID'], status=data['status'])
        
        url = reverse("controller:register_turtle", kwargs={"register_link": token.id})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        token_cleared = not Token.objects.filter(id=token.id).exists()
        self.assertTrue(token_cleared)

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "This turtle is already registered!"})

    def test_registration_accepted(self):
        """
        Request to register with a valid token are accepted. Token is deleted and turtle is added to database. 
        Response Status=200 and body contains an ID for the turtle
        """
        token = create_token(hours=0, minutes=0, seconds=0)
        data = {
            "name": "ExampleName",
            "computerID": "1234",
            "worldID": "1234",
            "status": True,
        }
        
        url = reverse("controller:register_turtle", kwargs={"register_link": token.id})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.content)

        turtle_registered = Turtle.objects.filter(computerID = data['computerID'], worldID = data['worldID'])
        self.assertTrue(turtle_registered)

        token_cleared = not Token.objects.filter(id=token.id).exists()
        self.assertTrue(token_cleared)
        self.assertEqual(response.status_code, 200)

        self.assertIn('id', response_data)
        try:
            uuid.UUID(response_data['id'], version=4)
            id_is_valid = True
        except ValueError:
            id_is_valid = False
        self.assertEqual(id_is_valid, True)

        
