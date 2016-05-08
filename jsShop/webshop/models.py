from django.db import models
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_dev = models.BooleanField(default = False)

class Game(models.Model):
	title = models.CharField(max_length = 255)
	author = models.ForeignKey(User)
	price = models.PositiveSmallIntegerField()
	Action='Action'
	Adventure='Adventure'
	Arcade='Arcade'
	Fighting='Fighting'
	Mini='Mini'
	Puzzle='Puzzle'
	Racing='Racing'
	Shooter='Shooter'
	Sport='Sport'
	Strategy='Strategy'
	Genres= (
		(Action, 'Action'),
		(Adventure, 'Adventure'),
		(Arcade, 'Arcade'),
		(Fighting, 'Fighting'),
		(Mini, 'Mini'),
		(Puzzle, 'Puzzle'),
		(Racing, 'Racing'),
		(Shooter, 'Shooter'),
		(Sport, 'Sport'),
		(Strategy, 'Strategy'),
	)
	picture=models.URLField(max_length = 600, default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg')
	tag = models.CharField(max_length = 255, choices = Genres)
	link = models.URLField(max_length = 200)
	description = models.TextField(max_length = 500)

class Leaderboard(models.Model):
	player = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	score = models.PositiveIntegerField()

class Payment(models.Model):
	STATUS = (
        ('success', 'success'),
        ('pending', 'pending'),
    )
	buyer = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	time = models.DateTimeField(default=datetime.now, blank=True)
	status = models.CharField(max_length = 255, choices = STATUS, default = 'pending')
	def create(self, buyer, game):
		self.buyer = buyer
		self.game = game
	def get_success_url(self):
		return 'success'
	def get_error_url(self):
		return 'error'
	def get_cancel_url(self):
		return 'cancel'

class Save(models.Model):
	player = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	game_state = models.TextField()
