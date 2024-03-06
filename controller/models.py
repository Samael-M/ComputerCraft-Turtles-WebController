from django.db import models
from datetime import timedelta
from django.utils import timezone
import uuid

class Turtle(models.Model): # Track individual turtles

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)  #unique ID for server to ID turtles

    computerID = models.IntegerField(default=0, unique=False) # Turtles in game ID
    worldID = models.IntegerField(default=0, unique=False) # ID of world turtle is in

    name = models.CharField(max_length=20)
    status = models.BooleanField() # true = online, false = offline

    class Meta:
        unique_together = (('computerID', 'worldID'),) #neither indivudally should necessarily be unique, but together they must

    # Do I need these or can turtle.status be used elsewhere in code?
    def is_online(self):
        return self.status
    def whoami(self):
        return self.name

class Command(models.Model): # Commands that can be sent
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    action_code = models.CharField(max_length=50) #actuall code to be sent | needed?

#Rethink what should be foreignKey
class SentCommands(models.Model): # Track the commands that have been sent
    name = models.ForeignKey(Turtle, on_delete=models.CASCADE)
    comand = models.ForeignKey(Command, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

#Rethink what should be foreignKey
class Log(models.Model): # log data/output received from turtle
    turtle = models.ForeignKey(Turtle, on_delete=models.CASCADE)
    log_text = models.TextField()
    timestamp = models.DateTimeField()

#This token is for validating registration links
class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField()

    def expired(self):
        time_valid = timedelta(hours=1)
        time_since_generation = timezone.now() - self.date
        return time_since_generation > time_valid
