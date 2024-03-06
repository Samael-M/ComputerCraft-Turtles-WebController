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
    Testing Token expired()
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
    
    def test_registration_rejected(self):
        """
        Request made to registration page without valid token are rejected
        """
        token = create_token(hours=-1, minutes=0, seconds=-1)
        url = reverse("controller:register_turtle", kwargs={"register_link": str(token.id)})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "Invalid token!"})

    def test_registration_accepted(self):
        """
        Request made to registration page is valid, token is accepted and response is sent
        """
        token = create_token(hours=0, minutes=0, seconds=0)
        request_data = {
            "name": "ExampleName",
            "computerID": "1234",
            "worldID": "1234",
            "status": True,
            "position": "ExamplePosition",
        }
        
        url = reverse("controller:register_turtle", kwargs={"register_link": str(token.id)})
        response = self.client.post(url, data=json.dumps(request_data), content_type='application/json')
        response_data = json.loads(response.content)

        self.assertIn('id', response_data)
        try:
            uuid.UUID(response_data['id'], version=4)
            id_is_valid = True
        except ValueError:
            id_is_valid = False
        
        self.assertEquals(id_is_valid, True)
        
