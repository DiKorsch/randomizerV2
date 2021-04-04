import datetime as dt
import random
import simplejson as json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone as tz
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET

from core.decorators import ensure_uuid
from core.models import Player

@require_GET
@ensure_uuid
def heartbeat(request):
	uuid = request.COOKIES[settings.ANONYMOUS_USER_COOKIE_ID]

	try:
		player = Player.objects.get(uuid=uuid)
		player.last_active = tz.now()
		player.save()

	except Player.DoesNotExist:
		pass

	return HttpResponse("")

@require_GET
def players(request):
	now = tz.now()
	diff = dt.timedelta(hours=1)

	data = {}
	players = Player.objects.filter(last_active__gte=now-diff)

	data["players"] = [p.to_json() for p in players]
	return JsonResponse(data)

class Randomize(View):

	GAME_FILE = "game.json"
	RND_TEAM = 0
	RND_NATION = "Random"

	NATIONS = [
		"Elben",
		"Isengard",
		"Menschen",
		"Mordor",
		"Orks",
		"Zwerge",
	]

	@method_decorator(login_required)
	def post(self, request):
		setup = json.loads(request.POST.get("json"))
		final_setup = self.randomize(setup)

		self.save_game(setup, final_setup)
		return self.get_current_game(request)

	def get(self, request):
		return self.get_current_game(request)

	def randomize(self, setup):
		final_setup = []
		for player in setup["players"]:
			final_player = dict(player)

			if player["nation"] == self.RND_NATION:
				final_player["nation"] = random.choice(self.NATIONS)

			final_setup.append(final_player)

		self.randomize_teams(final_setup, setup["n_teams"])
		return final_setup

	def randomize_teams(self, setup, n_teams):
		players_to_rnd = [player for player in setup if player["team"] == self.RND_TEAM]

		random.shuffle(players_to_rnd)

		for i, player in enumerate(players_to_rnd):
			player["team"] = i % n_teams + 1

	def save_game(self, setup, final_setup):
		with open(self.GAME_FILE, "w") as f:
			json.dump(dict(setup=setup, final_setup=final_setup), f, indent=2)

	def get_current_game(self, request):
		try:
			with open(self.GAME_FILE) as f:
				content = json.load(f)
		except FileNotFoundError:
			content = {}

		return JsonResponse(content)

