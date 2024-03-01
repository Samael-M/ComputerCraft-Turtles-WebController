from django.db import models

class Turtle(models.Model): # Track individual turtles
    name = models.CharField(max_length=20)
    worldID = models.IntegerField(default=0, unique=True)
    ComputerID = models.IntegerField(default=0, unique=True)
    status = models.BooleanField() # true = online, false = offline
    position = models.CharField(max_length=20) #probably don't want position represented as a string

    def is_online(self):
        return self.status
    def location(self):
        return self.position
    def whoami(self):
        return self.name

class Command(models.Model): # Commands that can be sent
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    action_code = models.CharField(max_length=50) #actuall code to be sent

class SentCommands(models.Model): # Track the commands that have been sent
    name = models.ForeignKey(Turtle, on_delete=models.CASCADE)
    comand = models.ForeignKey(Command, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class Log(models.Model): # log data/output received from turtle
    turtle = models.ForeignKey(Turtle, on_delete=models.CASCADE)
    log_text = models.TextField()
    timestamp = models.DateTimeField()