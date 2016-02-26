from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    is_dev = models.BooleanField(default = False)

class Game(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(User)
    price = models.PositiveSmallIntegerField()
    tag = models.CharField(max_length = 255)
    link = models.URLField(max_length = 200)

class Leaderboard(models.Model):
    player = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    score = models.PositiveIntegerField()

class Payment(models.Model):
    buyer = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    time = models.DateTimeField(auto_now = False)
